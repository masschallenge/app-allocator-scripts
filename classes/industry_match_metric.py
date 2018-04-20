from classes.metric import Metric

def industry_match(judge, application):
    return judge['industry'] == application['industry']

def industry_key(judge, application):
    return "Matching Industry"


class IndustryMatchMetric(Metric):
    output_key = industry_key
    condition = industry_match
