class FieldNeed(object):
    def __init__(self, field, option_states):
        self.field = field
        self.option_states = option_states

    def __str__(self):
        return "Field(%s, %s)" % (self.field,
                                  [str(state) for state in self.option_states])

    def __eq__(self, other):
        if isinstance(other, FieldNeed):
            return ((self.field == other.field) and
                    (self.option_states == other.option_states))
        return NotImplemented  # pragma: nocover

    def process_action(self, action, judge):
        option = judge.properties[self.field]
        for state in self.option_states:
            if option == state.option:
                state.process_action(action)

    def unsatisfied(self):
        return any([option_state.count > 0
                    for option_state in self.option_states])
