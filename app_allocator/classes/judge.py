from random import random
from app_allocator.classes.entity import Entity
from app_allocator.classes.property import Property
from app_allocator.classes.event import Event

CHANCE_OF_PASS = 0.04


class Judge(Entity):
    MAX_PANEL_SIZE = 10

    def __init__(self, data=None):
        super().__init__()
        self.applications = []
        self.type = "judge"
        for property in Property.all_properties:
            self.add_property(property, data)
        self.remaining = int(self.properties.get("commitment", 50))

    def complete_applications(self):
        events = []
        for application in self.applications:
            action = "finished"
            if self.passes(application):
                action = "pass"
            events.append(Event(action=action,
                                subject=self,
                                object=application,
                                description=self.properties))
        self.applications = []
        return events

    def passes(self, application):
        return random() <= CHANCE_OF_PASS

    def needs_another_application(self):
        return (self.remaining > 0 and
                len(self.applications) < Judge.MAX_PANEL_SIZE)

    def add_application(self, application):
        self.applications.append(application)
        result = Event(action="assigned",
                       subject=self,
                       object=application,
                       description=self.properties)
        self.remaining -= 1
        return result

    def mark_as_done(self):
        Event(action="done", subject=self)
        self.remaining = 0
