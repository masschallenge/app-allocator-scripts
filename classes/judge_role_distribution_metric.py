from classes.metric import Metric

def judge_role(judge, application):
    return "Judge Role %s" % judge['role']

class JudgeRoleDistributionMetric(Metric):
    name = "Judge Role"
    output_key = judge_role
