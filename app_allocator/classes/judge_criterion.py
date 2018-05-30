from app_allocator.classes.field_criterion import FieldCriterion
from app_allocator.classes.field_need import FieldNeed
from app_allocator.classes.option_state import OptionState


class JudgeCriterion(FieldCriterion):
    type = "judge"

    def __init__(self, name):
        super().__init__(name)

    def setup(self, judges, applications):
        pass

    def add_option(self, option, count, weight):
        if not option:
            raise NotImplementedError  # pragma: nocover
        super().add_option(option, count, weight)

    def as_need(self, application):
        return FieldNeed(self.name(),
                         [OptionState(spec.option, spec.count)
                          for spec in self.option_specs])

    
