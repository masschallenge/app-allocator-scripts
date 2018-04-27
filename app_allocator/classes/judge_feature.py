from app_allocator.classes.feature import Feature
from app_allocator.classes.option_state import OptionState


class JudgeFeature(Feature):
    def calc_initial_options(self, judges, applications):
        pass

    def option_states(self, _):
        return [OptionState(spec.option, spec.count)
                for spec in self.option_specs]
