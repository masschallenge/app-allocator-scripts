from app_allocator.classes.feature import Feature
from app_allocator.classes.option_spec import OptionSpec


class SpecificFeature(Feature):
    def __init__(self, field, count=1, option_specs=None):
        super().__init__(field, option_specs)
        self.count = count

    def option_counts(self, startup):
        option = startup.properties.get(self.field)
        if option is not None:
            if self.option_specs is None:
                return [(option, self.count)]
            else:
                return self.spec_count(option)
        return []

    def spec_count(self, option):
        for spec in self.option_specs:
            if spec.option == option:
                return [(option, spec.count)]
        return []

    def initial_options(self, judges, startups):
        if self.option_specs is None:
            self.option_specs = self.infer_option_specs(judges, startups)
        return [spec.option for spec in self.option_specs]

    def infer_option_specs(self, judges, startups):
        judge_options = self.options_with_counts(judges)
        startup_options = self.options_with_counts(startups)
        return sort_options(judge_options, startup_options)

    def options_with_counts(self, entities):
        options = {}
        for entity in entities:
            option = entity.properties.get(self.field)
            if option:
                value = options.get(option, 0) + 1
                options[option] = value
        return options


# options1 and options2 are expected to be dictionaries of
# options with counts.  E.g., {"Israel": 100, "Boston": 200}
# The result is the set of shared options ordered by the ratio
# of the count in options1 divided by the count in options2.
def sort_options(options1, options2):
    options = set(options1.keys()).intersection(options2.keys())
    weighted_options = [(options1[option]/float(options2[option]),
                         option) for option in options]
    return [OptionSpec(option) for _, option in sorted(weighted_options)]
