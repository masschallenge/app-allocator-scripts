from app_allocator.classes.event import Event
from app_allocator.classes.heuristic import Heuristic


class LinearSelection(Heuristic):
    'Simple and predictable heuristic for testing'
    name = "linear"

    def __init__(self, criteria=None):
        super().__init__()

    def setup(self, judges, applications):
        self.applications = applications
        self.judges = judges

    def work_left(self):
        return True

    def process_judge_events(self, events):
        pass

    def find_one_application(self, judge):
        if self.applications:
            application = self.applications.pop(0)
            return application

    def assess(self):
        Event(action="complete", description=LinearSelection.name)
