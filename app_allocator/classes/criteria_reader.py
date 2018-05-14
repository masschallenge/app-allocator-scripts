from csv import DictReader
from app_allocator.classes.judge_criterion import JudgeCriterion
from app_allocator.classes.matching_criterion import MatchingCriterion
from app_allocator.classes.feature_distribution import FeatureDistribution
from app_allocator.classes.reads_criterion import ReadsCriterion


DEFAULT_FILENAME = "criteria.csv"


class CriteriaReader(object):
    def __init__(self, filename):
        self.criteria = {}
        self.filename = filename
        if not self.filename:
            self.filename = DEFAULT_FILENAME
        self.read_data()

    def all(self):
        result = []
        for criteria_by_type in self.criteria.values():
            for criterion in criteria_by_type.values():
                result.append(criterion)
        return result

    def read_data(self):
        file = open(self.filename)
        for row in DictReader(file):
            self.process_row(row)
        file.close()

    def process_row(self, row):
        criterion = self.find_criterion(row["type"], row["name"])
        criterion.add_option(option=row.get("option"),
                             count=row.get("count"),
                             weight=row.get("weight"))

    def find_criterion(self, type, name):
        criteria_by_type = self.criteria.get(type)
        if not criteria_by_type:
            criteria_by_type = {}
            self.criteria[type] = criteria_by_type
        criterion = criteria_by_type.get(name)
        if not criterion:
            criterion = create_criterion(type, name)
            criteria_by_type[name] = criterion
        return criterion


def create_criterion(type, name):
    if name not in FeatureDistribution.all_distributions:
        FeatureDistribution(type, name)
    if type == "judge":
        return JudgeCriterion(name)
    if type == "matching":
        return MatchingCriterion(name)
    return ReadsCriterion(name)
