from copy import deepcopy
from math import log
from app_allocator.classes.assignments import has_been_assigned


class NeedsQueue(object):
    def __init__(self, needs={}, count=1):
        self.needs = deepcopy(needs)
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

    def judge_value(self, judge):
        value = 0
        application = self._next_application(judge)
        assignments = self.assignments.get(application, [])
        if application and self.needs:
            value = 0
            for need in self.needs:
                value += need.value_for_judge(judge, assignments)
            value *= (log(len(self.items)) + 1)
        return value

    def _next_application(self, judge):
        for application in self.items:
            if not has_been_assigned(judge, application):
                return application
        return None

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
