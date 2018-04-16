# Script for allocation a set of input judges to a set of input startups.
# Syntax:
# python3 allocate.py <csv-file>
# CSV file should be as created by generate.py

# TODO: Output should be as a CSV that can then assessed by a new assess.py
# script.
import csv
import sys
from random import choice

from classes.assignments import assign
from classes.event import Event
from classes.heuristic import find_heuristic
from classes.judge import Judge
from classes.startup import Startup


class Allocator(object):
    def __init__(self, filepath, heuristic):
        self.filepath = filepath
        self.judges = []
        self.startups = []
        self.heuristic = find_heuristic(heuristic)
        Event(action="heuristic",
              subject=self.heuristic.name)

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
            self.heuristic.process_judge_events(judge.complete_startups())
            while judge.needs_another_startup():
                startup = self.heuristic.find_one_startup(judge)
                if startup:
                    assign(judge, startup)
                else:
                    break
            if not judge.startups:
                judge.mark_as_done()
            if judge.remaining <= 0 and not judge.startups:
                self.judges.remove(judge)

    def assess(self):
        Event(action="done",
              subject="allocate.py",
              description="No more judges")
        self.heuristic.assess()
