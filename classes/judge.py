from random import random
from classes.entity import Entity
from classes.property import Property
from classes.event import Event

CHANCE_OF_PASS = 0.04


class Judge(Entity):
    MAX_PANEL_SIZE = 10

    def __init__(self, data=None):
        super().__init__()
        self.startups = []
        self.type = "judge"
        for property in Property.all_properties:
            self.add_property(property, data)
        self.add_fields_to_name(["industry", "program", "role", "gender"])
        self.remaining = int(self.properties.get("commitment", 50))

    def complete_startups(self):
        events = []
        for startup in self.startups:
            action = "finished"
            if self.passes(startup):
                action = "pass"
            events.append(Event(action=action,
                                subject=self,
                                object=startup))
        self.startups = []
        return events

    def passes(self, startup):
        return random() <= CHANCE_OF_PASS

    def needs_another_startup(self):
        return (self.remaining > 0 and
                len(self.startups) < Judge.MAX_PANEL_SIZE)

    def add_startup(self, startup):
        self.startups.append(startup)
        result = Event(action="assigned", subject=self, object=startup)
        self.remaining -= 1
        return result

    def mark_as_done(self):
        Event(action="done", subject=self)
        self.remaining = 0
