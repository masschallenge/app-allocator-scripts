from classes.bin import (
    BIN_DEFAULT_WEIGHT,
    Bin,
)


class IndustryBin(Bin):
    def __init__(self, value, weight=BIN_DEFAULT_WEIGHT):
        super().__init__(weight)
        self.industry = value

    def __str__(self):
        return "{} Industry Bin".format(self.industry)

    def match(self, startup):
        return startup.properties["industry"] == self.industry

    def weight(self, judge):
        if judge.properties["industry"] == self.industry:
            return super().weight(judge)
