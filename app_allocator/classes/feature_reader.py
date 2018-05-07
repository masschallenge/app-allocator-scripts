from csv import DictReader
from app_allocator.classes.judge_feature import JudgeFeature
from app_allocator.classes.matching_feature import MatchingFeature
from app_allocator.classes.reads_feature import ReadsFeature


DEFAULT_FILENAME = "feature.csv"


class FeatureReader(object):
    def __init__(self, filename):
        self.features = {}
        self.filename = filename
        if not self.filename:
            self.filename = DEFAULT_FILENAME
        self.read_data()

    def all(self):
        result = []
        for features_by_type in self.features.values():
            for feature in features_by_type.values():
                result.append(feature)
        return result

    def read_data(self):
        file = open(self.filename)
        for row in DictReader(file):
            self.process_row(row)
        file.close()

    def process_row(self, row):
        feature = self.find_feature(row["type"], row["name"])
        feature.add_option(option=row.get("option"),
                           count=row.get("count"),
                           weight=row.get("weight"))

    def find_feature(self, type, name):
        features_by_type = self.features.get(type)
        if not features_by_type:
            features_by_type = {}
            self.features[type] = features_by_type
        feature = features_by_type.get(name)
        if not feature:
            feature = create_feature(type, name)
            features_by_type[name] = feature
        return feature


def create_feature(type, name):
    if type == "judge":
        return JudgeFeature(name)
    if type == "matching":
        return MatchingFeature(name)
    return ReadsFeature(name)
