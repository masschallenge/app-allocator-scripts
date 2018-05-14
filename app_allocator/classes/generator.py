from app_allocator.classes.application import Application
from app_allocator.classes.feature_distribution import FeatureDistribution
from app_allocator.classes.judge import Judge


class Generator(object):
    def __init__(self, judge_count=0, application_count=0):
        FeatureDistribution.load_distributions()
        self.judges = [
            Judge(dists=FeatureDistribution.all_distributions.values())
            for i in range(judge_count)]
        self.applications = [
            Application(dists=FeatureDistribution.matching_distributions)
            for i in range(application_count)]
