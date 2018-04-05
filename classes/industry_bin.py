from classes.bin import (
    BIN_DEFAULT,
    Bin,
)


class IndustryBin(Bin):
    def __init__(self, industry, value=BIN_DEFAULT):
        super().__init__(value)
        self.industry = industry

    def __str__(self):
        return "{} Industry Bin".format(self.industry)

    def match(self, startup):
        return startup.properties["industry"] == self.industry

    def value(self, judge):
        if judge.properties["industry"] == self.industry:
            return super().value(judge)
