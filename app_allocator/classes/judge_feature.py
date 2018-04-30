from app_allocator.classes.feature import Feature
from app_allocator.classes.option_state import OptionState


class JudgeFeature(Feature):
    def calc_initial_options(self, judges, applications):
        pass

    def option_states(self, *args):
        return [OptionState(spec.option, spec.count)
                for spec in self.option_specs]

    def initial_need(self, startup, value):
        d =  dict([(spec.option, spec.count) for spec in self.option_specs])
        return d.get(value, 0)
