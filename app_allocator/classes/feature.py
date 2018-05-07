DEFAULT_COUNT = 1
DEFAULT_WEIGHT = 1


class Feature(object):
    def __init__(self, name):
        self.name = name
        self.count = DEFAULT_COUNT
        self.weight = DEFAULT_WEIGHT

    def setup(self, judges, applications):
        pass

    def add_option(self, option, count=None, weight=None):
        if count:
            self.count = int(count)
        if weight:
            self.weight = float(weight)
