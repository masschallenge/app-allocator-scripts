from app_allocator.classes.criterion import Criterion
from app_allocator.classes.option_spec import OptionSpec
from app_allocator.classes.read_need import ReadNeed


class ReadsCriterion(Criterion):
    type = "reads"

    def __init__(self, name):
        super().__init__(name)

    def as_need(self, application):
        return ReadNeed(count=self.count)

    def add_option(self, option, count, weight):
        super().add_option(option, count, weight)
        self.option_specs.add(OptionSpec(option, count, weight))
