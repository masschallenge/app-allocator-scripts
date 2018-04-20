from classes.metric import Metric

def judge_role(judge, application):
    return "Judge Role %s" % judge['role']

class JudgeRoleDistributionMetric(Metric):
    def __init__(self, role, target):
        super().__init__(target)
        self.name = "Judge Role"
        self.role = role

    def output_key(self):
        return "Role: %s" % self.role
    
    def condition(self, judge, application):
        return judge['role'] == self.role
    
