class LinearSelection(object):
    'Simple and predictable heuristic for testing'
    
    name = "linear"

    def setup(self, judges, startups):
        self.startups = startups
        self.judges = judges

    def work_left(self):
        return True

    def process_judge_events(self, events):
        pass

    def find_one_startup(self, judge):
        if self.startups:
            startup = self.startups.pop(0)
            return startup

    def assess(self):
        pass
