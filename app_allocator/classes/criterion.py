from collections import OrderedDict, defaultdict, Counter
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

    def evaluate(self,
                 assignments,
                 applications):
        app_needs_by_option = {}
        
        for spec in self.option_specs:
            needs = self._calc_initial_needs(applications, spec)
            spec_needs = spec.evaluate(assignments,
                                       needs,
                                       self.match_function(self.name(), spec.option))
            app_needs_by_option[spec.option] = spec_needs
        evaluation = {key: Counter(vals.values()) for key, vals in app_needs_by_option.items()}
        return {self.name(): evaluation}

    def _calc_initial_needs(self, applications, option_spec):
        needs = defaultdict(int)
        needs.update( {app: int(option_spec.count) for app in applications.values()})
        return needs
    
    def match_function(self, feature, option):
        def fn(judge, application):
            return True
        return fn

