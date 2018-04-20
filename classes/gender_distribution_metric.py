from classes.metric import Metric

class GenderDistributionMetric(Metric):
    def __init__(self, gender, target):
        super().__init__(target)
        self.gender = gender

    def output_key(self):
        return "Gender '%s'" % self.gender

    def condition(self, judge, application):
        return judge['gender'] == self.gender
    
