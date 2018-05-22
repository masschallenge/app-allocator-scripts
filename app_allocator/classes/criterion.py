from collections import OrderedDict
from sortedcontainers import SortedList
from app_allocator.classes.feature import Feature


DEFAULT_COUNT = 1
DEFAULT_WEIGHT = 1


class Criterion(object):
    all_criteria = {}
    
    def __init__(self, name):
        self.feature = Feature(type=self.type, name=name)
        self.count = DEFAULT_COUNT
        self.weight = DEFAULT_WEIGHT
        self.option_specs = SortedList()
        self.all_criteria[name] = self

    def name(self):
        return self.feature.name

    @classmethod
    def by_name(cls, name):
        return cls.all_criteria[name]
    
    def setup(self, judges, applications):
        pass

    def add_option(self, option, count, weight):
        if count != "":
            self.count = int(count)
        if weight != "":
            self.weight = float(weight)

    def initial_needs(self, application):
        needs = OrderedDict()
        for spec in self.option_specs:        
            needs[(self.name(), spec.option)] = float(spec.count)
        return needs
