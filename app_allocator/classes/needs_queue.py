from math import log
from app_allocator.classes.assignments import has_been_assigned
from app_allocator.classes.field_need import FieldNeed
from app_allocator.classes.option_state import OptionState


class NeedsQueue(object):
    def __init__(self, needs={}, count=1):
        self.needs = _copy_needs(needs)
        self.count = count
        self.counts = {}
        self.items = []
        self.name = str(self)
        self.assignments = {}

    def __str__(self):
        return "Q(%s)[%s]" % (",".join([str(need) for need in self.needs]),
                              len(self.items))

    def remaining(self):
        return len(self.items)

    def add_application(self, application, at_front=True):
        if at_front:
            self.items.insert(0, application)
        else:
            self.items.append(application)

    def move_to_end(self, application):
        if application in self.items:
            self.items.remove(application)
            self.items.append(application)

    def remove_application(self, application):
        self.items.remove(application)
        if application in self.assignments:
            self.assignments.pop(application)

    def remove_assignment(self, application, judge):
        assignments = self.assignments.get(application, [])
        if judge in assignments:
            assignments.remove(judge)

    def work_left(self):
        return len(self.items)

    def judge_value(self, judge, reads):
        value = 0
        application = self._next_application(judge)
        assignments = self.assignments.get(application, [])
        if application and self.needs:
            value = reads.read_value(application)
            for need in self.needs:
                judge_option = judge.properties[need.field]
                value += value_for_need(need,
                                        judge_option,
                                        assignments)
            value *= (log(len(self.items)) + 1)
        return value

    def _next_application(self, judge):
        for application in self.items:
            if not has_been_assigned(judge, application):
                return application
        return None

    def _assignment_count(self, application):
        top_assignments = self.assignments.get(application, [])
        if top_assignments:
            return len(top_assignments) + 1
        return 1

    def assign_next_application(self, judge):
        for application in self.items:
            if self._assign(judge, application):
                return application
        return None

    def _assign(self, judge, application):
        if not has_been_assigned(judge, application):
            self._add_assignment(judge, application)
            return application
        return None

    def _add_assignment(self, judge, application):
        assignments = self.assignments.get(application, [])
        assignments.append(judge)
        self.assignments[application] = assignments


def value_for_need(need, option, assignments):
    for option_state in need.option_states:
        if option_state.count > 0 and option == option_state.option:
            return adjust_for_assignments(assignments, need.field, option)
    return 0


def adjust_for_assignments(assignments, field, option):
    count = 0
    for judge in assignments:
        if judge.properties[field] == option:
            count += 1
    if count > 2:
        return 0
    return 1/(count + 1)


def _copy_needs(needs):
    result = []
    for need in needs:
        result.append(_copy_need(need))
    return result


def _copy_need(need):
    return FieldNeed(field=need.field,
                     option_states=_copy_option_states(need.option_states))


def _copy_option_states(options_states):
    result = []
    for state in options_states:
        result.append(_copy_option_state(state))
    return result


def _copy_option_state(option_state):
    return OptionState(option=option_state.option,
                       count=option_state.count)
