from classes.bin import (
    BIN_DEFAULT_WEIGHT,
    Bin,
)


class ReadsBin(Bin):
    def __init__(self, weight=BIN_DEFAULT_WEIGHT, count=1):
        super().__init__(weight=weight)
        self.count = count
        self.counts = {}

    def __str__(self):
        return "Read Bin"

    def add_startup(self, startup):
        matches = super().add_startup(startup)
        if matches:
            self.counts[startup.id()] = self.count
        return matches

    def update_startup(self, startup, keep=False):
        if not keep:
            count = self.counts[startup.id()]
            if count <= 1:
                super().update_startup(startup=startup, keep=False)
                return
            self.counts[startup.id()] = count - 1
        super().update_startup(startup, True)
