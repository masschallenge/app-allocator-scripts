from app_allocator.classes.feature import (
    DEFAULT_COUNT,
    DEFAULT_WEIGHT,
)


class OptionSpec(object):
    def __init__(self, option, count=DEFAULT_COUNT, weight=DEFAULT_WEIGHT):
        self.option = option
        self.count = count
        self.weight = weight
