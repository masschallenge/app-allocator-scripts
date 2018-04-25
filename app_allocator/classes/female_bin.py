from app_allocator.classes.bin import Bin

FEMALE_BIN_STRING = "At Least One Female Read Bin"


class FemaleBin(Bin):

    def __str__(self):
        return FEMALE_BIN_STRING

    def weight(self, judge):
        if judge.properties["gender"].startswith("f"):
            return super().weight(judge)
