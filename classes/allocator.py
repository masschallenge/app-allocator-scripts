# Script for allocation a set of input judges to a set of input startups.
# Syntax:
# python3 allocate.py <csv-file>
# CSV file should be as created by generate.py

# TODO: Output should be as a CSV that can then assessed by a new assess.py
# script.
import csv
import sys
from random import choice

from classes.heuristic import find_heuristic
from classes.judge import Judge
from classes.property import program
from classes.property import industry
from classes.startup import Startup


RANDOM_SELECTION_HEURISTIC = ""

class Allocator(object):
    def __init__(self, filepath, heuristic):
        self.filepath = filepath
        self.judges = []
        self.startups = []
        self.events = []
        self.heuristic = find_heuristic(heuristic)
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

    def setup(self):
        self.heuristic.setup(self.judges, self.startups)

    def allocate(self):
        while self.heuristic.work_left() and self.judges:
            judge = choice(self.judges)
            self.heuristic.next_action(judge)
            self.register_judge_events(judge)
            if not judge.has_more_work:
                self.judges.remove(judge)
            self.ticks += 1

    def register_judge_events(self, judge):
        while judge.events:
            self.add_event(judge.events.pop(0))

    def add_event(self, event):
        event.update(time=self.ticks)
        self.events.append(event)

    def assess(self):
        for event in self.events:
            print (event.to_csv())
        print("done,allocate.py,No more judges,")
        self.heuristic.assess()
