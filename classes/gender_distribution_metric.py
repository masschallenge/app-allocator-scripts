from classes.metric import Metric

def judge_gender(judge, application):
    return "Gender '%s'" % judge['gender']

class GenderDistributionMetric(Metric):
    name = "Gender"
    output_key = judge_gender
