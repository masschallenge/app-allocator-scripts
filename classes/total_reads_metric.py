from classes.metric import Metric

def industry_key(judge, application):
    return "Total Reads"

class TotalReadsMetric(Metric):
    output_key = industry_key

