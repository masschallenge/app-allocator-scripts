from random import random
from classes.assignments import assign
from classes.bin import BIN_NO_WEIGHT
from classes.entity import Entity
from classes.property import Property
from classes.event import Event

CHANCE_OF_PASS = 0.04


class Judge(Entity):
    MAX_PANEL_SIZE = 10

    def __init__(self, data=None):
        super().__init__()
        self.startups = []
        self.events = []
        self.type = "judge"
        for property in Property.all_properties:
            self.add_property(property, data)
        self.remaining = int(self.properties.get("commitment", 50))

    def next_action(self, bins):
        if self.startups:
            return self.finish_startups(bins)
        else:
            return self.find_startups(bins)

    def finish_startups(self, bins):
        for startup in self.startups:
            action = "finished"
            keep = False
            if self.passes(startup):
                action = "pass"
                keep = True
            self.add_event(action=action, startup=startup)
            for bin in bins:
                bin.update(self, startup, keep)
        self.startups = []
        self.has_more_work = True

    def passes(self, startup):
        return random() <= CHANCE_OF_PASS

    def find_startups(self, bins):
        while self.remaining > 0:
            self.find_one_startup(bins)
            if not self.has_more_work:
                break
        if not self.startups:
            self.add_event("done")
            self.remaining = 0
        self.has_more_work = self.startups != []

    def find_one_startup(self, bins):
        if len(self.startups) < Judge.MAX_PANEL_SIZE:
            startup = self.next_startup(bins)
            if startup:
                assign(self, startup)
                self.has_more_work = True
                return
        self.has_more_work = False

    def next_startup(self, bins):
        best_bin = self.best_bin(bins)
        if best_bin:
            startup = best_bin.next_startup(self)
            if startup:
                startup.update(bins, True)
                self.add_event("assigned", startup=startup, bin=best_bin)
                self.has_more_work = True
                return startup
            else:
                other_bins = [bin for bin in bins if bin != best_bin]
                startup = self.next_startup(other_bins)
                self.has_more_work = bool(startup)
                return startup
        return None

    def best_bin(self, bins):
        result = None
        highest_weight = BIN_NO_WEIGHT
        for bin in bins:
            weight = bin.adjusted_weight(self)
            if weight and weight > highest_weight:
                highest_weight = weight
                result = bin
        return result

    def add_event(self, action,
                  startup="",
                  bin=""):
        self.events.append(Event(action=action,
                                 judge=self,
                                 startup=startup,
                                 bin=bin))
