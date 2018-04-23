from app_allocator.classes.bin import (
    BIN_LOW_WEIGHT,
    Bin,
)


class SatisfiedBin(Bin):
    name_string = "Satisfied Bin"
    
    def __str__(self):
        return self.name_string

    def update_startup(self, startup, keep=False):
        super().update_startup(startup, True)

    def weight(self, judge):
        return BIN_LOW_WEIGHT

    def adjusted_weight(self, judge):
        return self.weight(judge)/float(self.capacity)
