from random import random
from classes.assignments import assign
from classes.bin import BIN_NO_WEIGHT
from classes.entity import Entity
from classes.property import Property


CHANCE_OF_PASS = 0.04


class Judge(Entity):
    MAX_PANEL_SIZE = 10

    def __init__(self, data=None):
        super().__init__()
        self.startups = []
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
            self.status_mesg = ("{action},{judge},{startup},".format(
                judge=self, action=action, startup=startup))
            for bin in bins:
                bin.update_startup(startup, keep)
        self.startups = []
        self.has_more_work = True

    def passes(self, startup):
        return random() <= CHANCE_OF_PASS

    def find_startups(self, bins):
        while self.remaining > 0:
            if not self.find_one_startup(bins):
                break
        if not self.startups:
            self.status_mesg = ("done,{judge},,".format(judge=self))
            self.remaining = 0
        self.has_more_work = self.startups != []

    def find_one_startup(self, bins):
        if len(self.startups) < Judge.MAX_PANEL_SIZE:
            startup = self.next_startup(bins)
            if startup:
                assign(self, startup)
                self.has_more_work = True
        self.has_more_work = False

    def next_startup(self, bins):
        best_bin = self.best_bin(bins)
        if best_bin:
            result = best_bin.next_startup(self)
            if result:
                result.update(bins, True)
                self.status_mesg = ("assigned,{judge},{startup},{bin}".format(
                        judge=self, startup=result, bin=best_bin))
                self.has_more_work = result
            else:
                other_bins = [bin for bin in bins if bin != best_bin]
                self.has_more_work = self.next_startup(other_bins)

    def best_bin(self, bins):
        result = None
        highest_weight = BIN_NO_WEIGHT
        for bin in bins:
            weight = bin.weight(self)
            if weight and weight > highest_weight:
                highest_weight = weight
                result = bin
        return result
