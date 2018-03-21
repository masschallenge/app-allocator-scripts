from classes.assignments import assign
from classes.bin import BIN_NO_VALUE
from classes.entity import Entity
from classes.property import Property


class Judge(Entity):
    def __init__(self, commitment=10, data=None):
        super().__init__()
        self.commitment = commitment
        self.startup = None
        self.type = "judge"
        for property in Property.all_properties:
            self.add_property(property, data)

    def __str__(self):
        return "Judge {}".format(self.id())

    def next_action(self, bins):
        if self.startup:
            return self.finish_startup(bins)
        else:
            return self.find_startup(bins)

    def finish_startup(self, bins):
        print("{judge} finished with {startup}".format(
                judge=self, startup=self.startup))
        for bin in bins:
            bin.update_startup(self.startup)
        self.startup = None
        return True

    def find_startup(self, bins):
        if self.commitment > 0:
            self.startup = self.next_startup(bins)
            if self.startup:
                assign(self, self.startup)
                self.commitment -= 1
                return True
        print("{judge} is done".format(judge=self))
        self.commitment = 0
        return False

    def next_startup(self, bins):
        best_bin = self.best_bin(bins)
        if best_bin:
            result = best_bin.next_startup(self)
            if result:
                result.update(bins, True)
                print("{judge} working on {startup} from {bin}".format(
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
