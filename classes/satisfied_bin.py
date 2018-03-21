from classes.bin import (
    BIN_LOW_VALUE,
    Bin,
)


class SatisfiedBin(Bin):
    def __str__(self):
        return "Satisfied Bin"

    def update_startup(self, startup, keep=False):
        super().update_startup(startup, True)

    def value(self, judge):
        return BIN_LOW_VALUE

    def status(self):
        print("Always statisfied")
