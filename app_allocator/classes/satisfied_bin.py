from app_allocator.classes.bin import (
    BIN_LOW_WEIGHT,
    Bin,
)


class SatisfiedBin(Bin):
    def __str__(self):
        return "Satisfied Bin"

    def update_startup(self, startup, keep=False):
        super().update_startup(startup, True)

    def weight(self, judge):
        return BIN_LOW_WEIGHT

    def adjusted_weight(self, judge):
        return self.weight(judge)/float(self.capacity)

    def status(self):
        print("success,{bin},Always statisfied,".format(bin=self))
