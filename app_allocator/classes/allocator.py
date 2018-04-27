# Script for allocation a set of input judges to a set of input applications.
# Syntax:
# python3 allocate.py <csv-file>
# CSV file should be as created by generate.py

# TODO: Output should be as a CSV that can then assessed by a new assess.py
# script.
import csv
import sys
from random import choice

from app_allocator.classes.assignments import assign
from app_allocator.classes.heuristic import find_heuristic
from app_allocator.classes.judge import Judge
from app_allocator.classes.application import Application


class Allocator(object):
    def __init__(self, filepath, heuristic):
        self.filepath = filepath
        self.judges = []
        self.applications = []
        self.heuristic = find_heuristic(heuristic)

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
                elif row["type"] == "application":
                    self.applications.append(Application(data=row))

    def setup(self):
        self.heuristic.setup(self.judges, self.applications)

    def allocate(self):
        while self.heuristic.work_left() and self.judges:
            judge = choice(self.judges)
            self.heuristic.process_judge_events(judge.complete_applications())
            self.assign_applications(judge)
            if judge.remaining <= 0 and not judge.applications:
                self.judges.remove(judge)

    def assign_applications(self, judge):
        while judge.needs_another_application():
            application = self.heuristic.find_one_application(judge)
            if application:
                assign(judge, application)
            else:
                break
        if not judge.applications:
            judge.mark_as_done()

    def assess(self):
        self.heuristic.assess()
