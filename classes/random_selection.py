from random import choice

from classes.assignments import assign


class RandomSelection(object):
    name = "random"

    def setup(self, judges, startups):
        self.startups = startups

    def work_left(self):
        return True

    def next_action(self, judge):
        judge.complete_startups()
        while judge.needs_another_startup():
            assign(judge, choice(self.startups))

    def assess(self):
        pass
