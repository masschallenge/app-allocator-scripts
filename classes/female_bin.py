from classes.bin import (
    BIN_HIGH_WEIGHT,
    Bin,
)


class FemaleBin(Bin):
    def __str__(self):
        return "At Least One Female Read Bin"

    def weight(self, judge):
        if judge.properties["gender"] == "female":
            return super().weight(judge)
