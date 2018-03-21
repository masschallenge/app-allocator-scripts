from classes.bin import (
    BIN_HIGH_VALUE,
    Bin,
)


class FemaleBin(Bin):
    def __str__(self):
        return "At Least One Female Read Bin"

    def value(self, judge):
        if judge.properties["gender"] == "female":
            return BIN_HIGH_VALUE
