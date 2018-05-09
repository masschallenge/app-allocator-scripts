from app_allocator.classes.industry_match_metric import IndustryMatchMetric
from app_allocator.classes.judge import Judge
from app_allocator.classes.application import Application

INDUSTRY = "Stargazing"
TARGET = 3


class TestIndustryMatchMetric(object):
    def test_condition(self):
        metric = IndustryMatchMetric(TARGET)
        judge = Judge()
        application = Application()
        application.properties['industry'] = judge['industry']
        assert metric.condition(judge, application)
