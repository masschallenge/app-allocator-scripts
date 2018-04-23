from app_allocator.classes.metric import Metric


class IndustryMatchMetric(Metric):
    def condition(self, judge, application):
        return judge['industry'] == application['industry']

    def output_key(self):
        return "Matching Industry"
