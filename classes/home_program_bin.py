from classes.bin import (
    BIN_DEFAULT_WEIGHT,
    Bin,
)


class HomeProgramBin(Bin):
    name_format = "{} Home Program Bin"

    def __init__(self, value, weight=BIN_DEFAULT_WEIGHT):
        super().__init__(weight)
        self.program = value

    def __str__(self):
        return self.name_format.format(self.program)

    def match(self, entity):
        return entity.properties['program'] == self.program
