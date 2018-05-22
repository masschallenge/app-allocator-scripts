from functools import total_ordering
from app_allocator.classes.criterion import (
    DEFAULT_COUNT,
    DEFAULT_WEIGHT,
)

@total_ordering
class OptionSpec(object):
    def __init__(self, option, count=DEFAULT_COUNT, weight=DEFAULT_WEIGHT):
        self.option = option
        self.count = count
        self.weight = weight

    def __eq__(self, other):
        return self.option == other.option

    def __ne__(self, other):
        return self.option != other.option

    def __lt__(self, other):
        return self.option < other.option
