from classes.bin import (
    BIN_DEFAULT_WEIGHT,
    BIN_NO_WEIGHT,
    Bin,
)


class HomeProgramBin(Bin):
    name_format = "{} Home Program Bin"

    def __init__(self, value, weight=BIN_DEFAULT_WEIGHT):
        super().__init__(weight)
        self.program = value

    def __str__(self):
        return self.name_format.format(self.program)

    def match(self, startup):
        return startup.properties['program'] == self.program

    def weight(self, judge):
        if judge.properties['program'] == self.program:
            return super().weight(judge)
        else:
            return BIN_NO_WEIGHT
