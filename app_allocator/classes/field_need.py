class FieldNeed(object):
    def __init__(self, field, option_states):
        self.field = field
        self.option_states = option_states

    def __str__(self):
        return "F(%s, [%s])" % (self.field,
                                ",".join([str(state)
                                          for state in self.option_states]))

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

    def value_for_judge(self, judge, assignments):
        option = judge.properties.get(self.field)
        for option_state in self.option_states:
            if option_state.count > 0 and option == option_state.option:
                return self.adjust_for_assignments(assignments, option)
        return 0

    def adjust_for_assignments(self, assignments, option):
        count = 0
        for judge in assignments:
            if judge.properties[self.field] == option:
                count += 1
            if count > 2:
                return 0
        return 1/(count + 1)
