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
                for option_state in need.option_states:
                    if judge_option == option_state.option:
                        value += 1/(option_state.assigned + 1)
        return value
            
    def assign(self, judge, startup, needs):
        if not has_been_assigned(judge, startup):
            self.add_assignment(judge, startup, needs)
            return startup
        return None

    def add_assignment(self, judge, startup, needs):
        for need in needs:
            need.process_action("assign", judge)

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
