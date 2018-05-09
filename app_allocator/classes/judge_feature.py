from app_allocator.classes.feature import Feature
from app_allocator.classes.field_need import FieldNeed
from app_allocator.classes.option_state import OptionState


class JudgeFeature(Feature):
    def setup(self, judges, applications):
        pass

    def as_need(self, application):
        return FieldNeed(self.field,
                         [OptionState(spec.option, spec.count)
                          for spec in self.option_specs])
