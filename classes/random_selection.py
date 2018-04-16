from random import choice


class RandomSelection(object):
    name = "random"

    def setup(self, judges, startups):
        self.startups = startups

    def work_left(self):
        return True

    def process_judge_events(self, events):
        pass

    def find_one_startup(self, judge):
        return choice(self.startups)

    def assess(self):
        pass
