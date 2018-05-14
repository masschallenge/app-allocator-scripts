from random import choice
from app_allocator.classes.event import Event
from app_allocator.classes.heuristic import Heuristic

class RandomSelection(Heuristic):
    name = "random"
    BATCH_HEURISTIC = False

    def setup(self, judges, applications):
        self.applications = applications

    def work_left(self):
        return True

    def process_judge_events(self, events):
        pass

    def find_one_application(self, judge):
        return choice(self.applications)

    def assess(self):
        Event(action="complete", description=RandomSelection.name)

Heuristic.register_heuristic(RandomSelection)
