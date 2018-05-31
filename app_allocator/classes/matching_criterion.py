from collections import OrderedDict
from app_allocator.classes.field_criterion import FieldCriterion
from app_allocator.classes.field_need import FieldNeed
from app_allocator.classes.option_spec import OptionSpec
from app_allocator.classes.option_state import OptionState


class MatchingCriterion(FieldCriterion):
    type = "matching"
    all_matching_criteria = {}

    def __init__(self, name):
        super().__init__(name)
        MatchingCriterion.all_matching_criteria[name] = self

    def as_need(self, application):
        return FieldNeed(self.name(), self.option_states(application))

    def option_states(self, application):
        option = application.properties.get(self.name())
        if option is not None:
            if self.option_specs:
                return self._states_from_specs(option)
            else:
                return [OptionState(option, self.count)]
        return []

    def _states_from_specs(self, option):
        for spec in self.option_specs:
            if spec.option == option:
                return [OptionState(option, spec.count)]
        return []  # pragma: nocover

    def setup(self, judges, applications):
        if not self.option_specs:
            self.option_specs = self._infer_option_specs(judges, applications)

    def _infer_option_specs(self, judges, applications):
        judge_options = self._options_with_counts(judges)
        judge_keys = set(judge_options.keys())
        app_options = self._options_with_counts(applications)
        app_keys = set(app_options.keys())
        shared_options = judge_keys.intersection(app_keys)
        weighted_options = [(judge_options[option]/float(app_options[option]),
                             option) for option in shared_options]
        return [OptionSpec(option=option, weight=self.weight) for _, option in
                sorted(weighted_options, key=lambda pair: pair[0])]

    @classmethod
    def set_up_all(cls, judges, applications):
        for criterion in cls.all_matching_criteria.values():
            criterion.setup(judges, applications)

    def _options_with_counts(self, entities):
        options = {}
        for entity in entities:
            option = entity.properties.get(self.name())
            if option:
                value = options.get(option, 0) + 1
                options[option] = value
        return options

    def initial_needs(self, application):
        needs = OrderedDict()
        for spec in self.option_specs:
            if application[self.name()] == spec.option:
                needs[(self.name(), spec.option)] = float(spec.count)
            else:
                needs[(self.name(), spec.option)] = 0.0
        return needs
