from classes.assignments import has_been_assigned


class Queue(object):
    def __init__(self, constraints={}, count=1):
        self.constraints = constraints.copy()
        self.count = count
        self.counts = {}
        self.items = []
        self.assigned = {}

    def __str__(self):
        return "Queue(%s)" % self.constraints

    def add_constraint(self, constraint):
        self.constraints.update(constraint)

    def add_if_matches(self, entity):
        for feature, option in self.constraints.items():
            if entity.properties.get(feature) != option:
                return
        self.items.append(entity)

    def next_item(self, judge):
        if not self.matches(judge):
            return None
        index = 0
        count = len(self.items)
        while index < count:
            startup = self.items[index]
            if not has_been_assigned(judge, startup):
                self.add_assignment(judge, startup)
                self.items.remove(startup)
                return startup
            index += 1
        return None

    def matches(self, judge):
        if not self.constraints:
            return True
        for field, option in self.constraints.items():
            if judge.properties.get(field) == option:
                return True
        return False

    def add_assignment(self, judge, startup):
        assignments = self.assigned.get(startup, [])
        assignments.append(judge)
        self.assigned[startup] = assignments

    def process_action(self, action, judge, startup):
        judges = self.assigned.get(startup, [])
        if judge in judges:
            if action == "finished":
                self.requeue(judge, startup, 1)
            elif action == "pass":
                self.requeue(judge, startup, 0)
            self.assigned[startup].remove(judge)

    def requeue(self, judge, startup, increment):
        count = self.counts.get(startup, 0) + increment
        if count < self.count:
            self.counts[startup] = count
            self.items.append(startup)


def extended_queue(queue, constraint):
    result = Queue(queue.constraints)
    result.add_constraint(constraint)
    return result
