from random import random
from app_allocator.classes.entity import Entity
from app_allocator.classes.property import Property
from app_allocator.classes.event import Event

# This is based on a comparison of commitment to completed for 2017
# We should eventually compute this from the actual data
DEFAULT_CHANCE_OF_PASS = 0.152773932


class Judge(Entity):
    MAX_PANEL_SIZE = 10

    def __init__(self, data=None, chance_of_pass=DEFAULT_CHANCE_OF_PASS):
        super().__init__()
        self.all_applications = []
        self.current_applications = []
        self.chance_of_pass = chance_of_pass
        self.type = "judge"
        for property in Property.all_properties:
            self.add_property(property, data)
        self.remaining = int(self.properties.get("commitment", 50))

    def complete_applications(self):
        events = []
        for application in self.current_applications:
            action = "finished"
            if self.passes(application):
                action = "pass"
            events.append(Event(action=action,
                                subject=self,
                                object=application,
                                description=self.properties))
        self.current_applications = []
        return events

    def passes(self, application):
        return random() <= self.chance_of_pass

    def request_batch(self, heuristic):
        batch_size = min(self.remaining, self.MAX_PANEL_SIZE)
        return heuristic.request_batch(self, batch_size)

    def needs_another_application(self):
        return (self.remaining > 0 and
                len(self.current_applications) < Judge.MAX_PANEL_SIZE)

    def add_application(self, application):
        self.current_applications.append(application)
        self.all_applications.append(application)
        result = Event(action="assigned",
                       subject=self,
                       object=application,
                       description=self.properties)
        self.remaining -= 1
        return result

    def mark_as_done(self):
        Event(action="done", subject=self)
        self.remaining = 0

    def zscore(self):
        return float(self.properties.get("zscore", 0.0))
