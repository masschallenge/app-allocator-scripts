from random import choice


class RandomSelection(object):
    name = "random"

    def setup(self, judges, applications):
        self.applications = applications

    def work_left(self):
        return True

    def process_judge_events(self, events):
        pass

    def find_one_application(self, judge):
        return choice(self.applications)

    def assess(self):
        pass
