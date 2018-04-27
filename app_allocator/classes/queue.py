from app_allocator.classes.assignments import has_been_assigned


class Queue(object):
    def __init__(self, needs={}, count=1):
        self.needs = needs.copy()
        self.count = count
        self.counts = {}
        self.items = []

    def __str__(self):
        return "Queue(%s)" % [str(need) for need in self.needs]

    def judge_value(self, judge):
        value = 0
        if self.needs:
            for need in self.needs:
                judge_option = judge.properties[need.field]
                value += option_state_value(need.option_states,
                                            judge_option)
        return value

    def assign(self, judge, application, needs):
        if not has_been_assigned(judge, application):
            self.add_assignment(judge, application, needs)
            return application
        return None

    def add_assignment(self, judge, application, needs):
        for need in needs:
            need.process_action("assign", judge)


def option_state_value(option_states, option):
    value = 0
    for option_state in option_states:
        if option == option_state.option:
            value += 1/(option_state.assigned + 1)
    return value
