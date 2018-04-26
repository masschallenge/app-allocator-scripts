from app_allocator.classes.feature import Feature
from app_allocator.classes.option_state import OptionState


class UniversalFeature(Feature):
    def initial_options(self, judges, startups):
        return []

    def option_states(self, _):
        return [OptionState(spec.option, spec.count)
                for spec in self.option_specs]
