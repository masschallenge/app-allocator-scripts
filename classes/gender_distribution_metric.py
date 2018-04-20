from classes.metric import Metric

class GenderDistributionMetric(Metric):
    def __init__(self, gender, target):
        super().__init__()
        self.gender = gender
        self.target = target

    def output_key(self):
        return "Gender '%s'" % self.gender

    def condition(self, judge, application):
        return judge['gender'] == self.gender
    
