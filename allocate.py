import csv
import sys
from random import shuffle

from classes.female_bin import FemaleBin
from classes.judge import Judge
from classes.reads_bin import ReadsBin
from classes.satisfied_bin import SatisfiedBin
from classes.startup import Startup


def read_entities(filename):
    judges = []
    startups = []
    with open(filename, newline="") as csvfile:
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


def work_left(bins):
    for bin in bins:
        if bin.work_left():
            return True
    return False


judges, startups = read_entities(sys.argv[1])
bins = [ReadsBin(), SatisfiedBin(), FemaleBin()]
add_startups(startups, bins)


while work_left(bins):
    judges = [judge for judge in judges if judge.commitment > 0]
    shuffle(judges)
    actions_taken = 0
    for judge in judges:
        if judge.next_action(bins):
            actions_taken += 1
    if actions_taken == 0:
        print("No actions taken")
        break

for bin in bins:
    bin.status()
