from app_allocator.classes.criterion import Criterion
from app_allocator.classes.option_spec import OptionSpec


class FieldCriterion(Criterion):
    def __init__(self, name):
        super().__init__(name)

    def add_option(self, option, count=None, weight=None):
        if option:
            self.option_specs.add(OptionSpec(option, count, weight))
        else:
            super().add_option(option, count, weight)
