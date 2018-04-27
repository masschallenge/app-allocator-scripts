from app_allocator.classes.metric import Metric


class JudgeRoleDistributionMetric(Metric):
    def __init__(self, role, target):
        super().__init__(target)
        self.name = "Judge Role"
        self.role = role

    def output_key(self):
        return "Role: %s" % self.role

    def condition(self, judge, application):
        return judge['role'] == self.role
