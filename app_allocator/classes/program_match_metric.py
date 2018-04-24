from app_allocator.classes.metric import Metric


class ProgramMatchMetric(Metric):
    def output_key(self):
        return "Home Program Reads"

    def condition(self, judge, application):
        return judge['program'] == application['program']
