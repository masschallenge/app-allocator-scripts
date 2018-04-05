from classes.assignments import assign
from classes.bin import BIN_NO_VALUE
from classes.entity import Entity
from classes.property import Property


class Judge(Entity):
    MAX_PANEL_SIZE = 10

    def __init__(self, data=None):
        super().__init__()
        self.startups = []
        self.type = "judge"
        for property in Property.all_properties:
            self.add_property(property, data)
        self.commitment = int(self.properties.get("commitment", 50))

    def __str__(self):
        return "Judge {}".format(self.id())

    def next_action(self, bins):
        if self.startups:
            return self.finish_startups(bins)
        else:
            return self.find_startups(bins)

    def finish_startups(self, bins):
        for startup in self.startups:
            print("{judge},finished,{startup},".format(
                    judge=self, startup=startup))
            for bin in bins:
                bin.update_startup(startup)
        self.startups = []
        return True

    def find_startups(self, bins):
        while self.commitment > 0:
            if len(self.startups) >= Judge.MAX_PANEL_SIZE:
                break
            startup = self.next_startup(bins)
            if startup:
                assign(self, startup)
            else:
                break
        if not self.startups:
            print("{judge},done,,".format(judge=self))
            self.commitment = 0
        return self.startups != []

    def next_startup(self, bins):
        best_bin = self.best_bin(bins)
        if best_bin:
            result = best_bin.next_startup(self)
            if result:
                result.update(bins, True)
                print("{judge},assigned,{startup},{bin}".format(
                        judge=self, startup=result, bin=best_bin))
                return result
            else:
                other_bins = [bin for bin in bins if bin != best_bin]
                return self.next_startup(other_bins)

    def best_bin(self, bins):
        result = None
        best_value = BIN_NO_VALUE
        for bin in bins:
            value = bin.value(self)
            if value and value > best_value:
                best_value = value
                result = bin
        return result
