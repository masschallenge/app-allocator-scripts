from app_allocator.classes.feature import Feature
from app_allocator.classes.option_spec import OptionSpec


class FieldFeature(Feature):
    def __init__(self, name):
        super().__init__(name)
        self.option_specs = []

    def add_option(self, option, count=None, weight=None):
        if option:
            self.option_specs.append(OptionSpec(option, count, weight))
        else:
            super().add_option(option, count, weight)
