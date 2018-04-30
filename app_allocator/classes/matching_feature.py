from app_allocator.classes.feature import Feature
from app_allocator.classes.option_spec import OptionSpec
from app_allocator.classes.option_state import OptionState


class MatchingFeature(Feature):
    def __init__(self, field, count=1, option_specs=None):
        super().__init__(field, option_specs)
        self.count = count

    def option_states(self, application):
        option = application.properties.get(self.field)
        if option is not None:
            if self.option_specs is None:
                return [OptionState(option, self.count)]
            else:
                return self._states_from_specs(option)
        return []

    def _states_from_specs(self, option):
        for spec in self.option_specs:
            if spec.option == option:
                return [OptionState(option, spec.count)]
        return []

    def calc_initial_options(self, judges, applications):
        if self.option_specs is None:
            self.option_specs = self._infer_option_specs(judges, applications)

    def _infer_option_specs(self, judges, applications):
        judge_options = self._options_with_counts(judges)
        application_options = self._options_with_counts(applications)
        return _shared_options_by_scarcity(judge_options, application_options)

    def _options_with_counts(self, entities):
        options = {}
        for entity in entities:
            option = entity.properties.get(self.field)
            if option:
                value = options.get(option, 0) + 1
                options[option] = value
        return options

    def initial_need(self, startup, value):
        if startup.properties.get(self.field) == value:
            return self.count
        else:
            return 0

# options1 and options2 are expected to be dictionaries of
# options with counts.  E.g., {"Israel": 100, "Boston": 200}
# The result is the set of shared options ordered by the ratio
# of the count in options1 divided by the count in options2.
def _shared_options_by_scarcity(options1, options2):
    shared_options = set(options1.keys()).intersection(options2.keys())
    weighted_options = [(options1[option]/float(options2[option]),
                         option) for option in shared_options]
    return [OptionSpec(option) for _, option in
            sorted(weighted_options, key=lambda pair: pair[0])]
