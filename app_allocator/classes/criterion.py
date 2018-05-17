from app_allocator.classes.feature import Feature


DEFAULT_COUNT = 1
DEFAULT_WEIGHT = 1


class Criterion(object):
    def __init__(self, name):
        self.feature = Feature(type=self.type, name=name)
        self.count = DEFAULT_COUNT
        self.weight = DEFAULT_WEIGHT

    def name(self):
        return self.feature.name

    def setup(self, judges, applications):
        pass

    def add_option(self, option, count=None, weight=None):
        if count:
            self.count = int(count)
        if weight:
            self.weight = float(weight)
