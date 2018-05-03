from app_allocator.classes.feature import Feature
from app_allocator.classes.field_need import FieldNeed
from app_allocator.classes.option_state import OptionState


class JudgeFeature(Feature):
    def setup(self, judges, applications):
        pass


    def option_states(self, *args):
        return [OptionState(spec.option, spec.count)
                for spec in self.option_specs]

    def initial_need(self, startup, value):
        d =  dict([(spec.option, spec.count) for spec in self.option_specs])
        return float(d.get(value, 0))

    def option_states(self, _):
        return [OptionState(spec.option, spec.count)
                for spec in self.option_specs]

    def as_need(self, _):
        return FieldNeed(self.field,
                         [OptionState(spec.option, spec.count)
                          for spec in self.option_specs])

