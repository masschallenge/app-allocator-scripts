from classes.bin import (
    BIN_DEFAULT,
    Bin,
)


class HomeProgramBin(Bin):
    name_format = "{} Home Program Bin"
    
    def __init__(self, program, value=BIN_DEFAULT):
        super().__init__(value)
        self.program = program

    def __str__(self):
        return self.name_format.format(self.program)

    def match(self, startup):
        return startup.properties['program'] == self.program

    def value(self, judge):
        if judge.properties['industry'] == self.program:
            return super().value(judge)
        else:
            #None? mixed-type returns are ugly
            pass
            


