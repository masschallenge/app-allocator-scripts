# Script for allocation a set of input judges to a set of input startups.
# Syntax:
# python3 allocate.py <csv-file>
# CSV file should be as created by generate.py

# TODO: Output should be as a CSV that can then assessed by a new assess.py
# script.
import csv
import sys
from random import choice

from classes.bin import BIN_DEFAULT_WEIGHT
from classes.female_bin import FemaleBin
from classes.home_program_bin import HomeProgramBin
from classes.industry_bin import IndustryBin
from classes.judge import Judge
from classes.property import program
from classes.property import industry
from classes.reads_bin import ReadsBin
from classes.role_bin import RoleBin
from classes.satisfied_bin import SatisfiedBin
from classes.startup import Startup


def read_entities(file):
    judges = []
    startups = []
    with file as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["type"] == "judge":
                judges.append(Judge(data=row))
            elif row["type"] == "startup":
                startups.append(Startup(data=row))
    return judges, startups


def add_startups(startups, bins):
    for startup in startups:
        for bin in bins:
            bin.add_startup(startup)


def calc_capacity(judges, bins):
    for bin in bins:
        bin.calc_capacity(judges)


def work_left(bins):
    for bin in bins:
        if bin.work_left():
            return True
    return False


def bin_factory(klass, values, weight):
    return [klass(value=value, weight=weight)
            for value in values]


if len(sys.argv) > 1:
    file = open(sys.argv[1], newline="")
else:
    file = sys.stdin

judges, startups = read_entities(file)

FEMALE_WEIGHT = 2
ROLE_WEIGHT = 3
HOME_PROGRAM_WEIGHT = 4
JUDGE_ZSCORE_WEIGHT = 5
INDUSTRY_WEIGHT = 2

bins = ([ReadsBin(count=4),
         FemaleBin(weight=FEMALE_WEIGHT*BIN_DEFAULT_WEIGHT),
         SatisfiedBin(),
         RoleBin(value="Executive",
                 weight=ROLE_WEIGHT*BIN_DEFAULT_WEIGHT,
                 count=2),
         RoleBin(value="Lawyer",
                 weight=ROLE_WEIGHT*BIN_DEFAULT_WEIGHT),
         RoleBin(value="Investor",
                 weight=ROLE_WEIGHT*BIN_DEFAULT_WEIGHT)] +
        bin_factory(IndustryBin,
                    values=[value for value, _ in industry.values],
                    weight=INDUSTRY_WEIGHT*BIN_DEFAULT_WEIGHT) +
        bin_factory(HomeProgramBin,
                    values=[value for value, _ in program.values],
                    weight=HOME_PROGRAM_WEIGHT*BIN_DEFAULT_WEIGHT))

add_startups(startups, bins)
calc_capacity(judges, bins)


while work_left(bins):
    if not judges:
        print("done,allocate.py,No more judges,")
        break
    judge = choice(judges)
    if not judge.next_action(bins):
        judges.remove(judge)

# Assessor
for bin in bins:
    bin.status()
