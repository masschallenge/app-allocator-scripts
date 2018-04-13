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
from classes.satisfied_bin import SatisfiedBin
from classes.startup import Startup



class Allocator(object):
    def __init__(self, filepath=None):
        self.filepath = filepath
        self.judges = []
        self.startups = []
        self.bins = []
        self.events = []
        self.ticks = 0


    def _file(self):
        if self.filepath is None:
            return sys.stdin
        else:
            return open(self.filepath)
        
    def read_entities(self):
        with self._file() as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["type"] == "judge":
                    self.judges.append(Judge(data=row))
                elif row["type"] == "startup":
                    self.startups.append(Startup(data=row))

    def add_startups(self):
        for startup in self.startups:
            for bin in self.bins:
                bin.add_startup(startup)

    def work_left(self):
        return any([bin.work_left() for bin in self.bins])

    def default_bins(self):
        self.bins = (
            [ReadsBin(),
             FemaleBin(weight=2*BIN_DEFAULT_WEIGHT),
             SatisfiedBin()] +
            bin_factory(IndustryBin,
                        values=[value for value, _ in industry.values],
                        weight=4*BIN_DEFAULT_WEIGHT) +
            bin_factory(HomeProgramBin,
                        values=[value for value, _ in program.values],
                        weight=3*BIN_DEFAULT_WEIGHT))

        
    def allocate (self):
        while self.work_left() and self.judges:
            judge = choice(self.judges)
            judge.next_action(self.bins)
            self.register_judge_events(judge)
            if not judge.has_more_work:
                self.judges.remove(judge)
            self.ticks += 1

    def register_judge_events(self, judge):
        while judge.events:
            self.add_event(judge.events.pop(0))
            
    def assess_allocations(self):
        for event in self.events:
            print (event.to_csv())
        print("done,allocate.py,No more judges,")

    def assess_bins(self):
        for bin in self.bins:
            bin.status()

    def add_event(self, event):
        event.update(time=self.ticks)
        self.events.append(event)
                
def bin_factory(klass, values, weight):
    return [klass(value=value, weight=weight)
            for value in values]


