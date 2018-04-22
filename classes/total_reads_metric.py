from classes.metric import Metric


class TotalReadsMetric(Metric):
    def output_key(self):
        return "Total Reads"
