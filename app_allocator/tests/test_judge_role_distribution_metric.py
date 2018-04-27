from app_allocator.classes.industry_match_metric import IndustryMatchMetric
from app_allocator.classes.judge import Judge
from app_allocator.classes.startup import Startup

INDUSTRY = "Stargazing"
TARGET = 3


class TestIndustryMatchMetric(object):
    def test_condition(self):
        metric = IndustryMatchMetric(TARGET)
        judge = Judge()
        startup = Startup()
        startup.properties['industry'] = judge['industry']
        assert metric.condition(judge, startup)
