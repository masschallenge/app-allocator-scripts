from app_allocator.classes.bin import (
    BIN_DEFAULT_WEIGHT,
    Bin,
)

class ReadsBin(Bin):
    def __init__(self, weight=BIN_DEFAULT_WEIGHT, count=1):
        super().__init__(property_name="reads",
                         property_value="",
                         weight=weight)
        self.count = count
        self.counts = {}

    def match(self, judge):
        return True
    
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
