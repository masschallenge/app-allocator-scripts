from csv import DictReader
from random import random


JUDGE_TYPE = "judge"
MATCHING_TYPE = "matching"
NAME_TYPE = "name"
READS_TYPE = "reads"


class FeatureDistribution(object):
    all_distributions = {}
    matching_distributions = []

    def __init__(self, type, name, values=None):
        self.type = type
        self.name = name
        self.values = values
        self.weights = {}
        self.total = 0
        FeatureDistribution.all_distributions[name] = self
        if type == MATCHING_TYPE:
            FeatureDistribution.matching_distributions.append(self)

    @classmethod
    def load_distributions(self, file):
        reader = DictReader(file)
        for row in reader:
            name = row["name"]
            distribution = FeatureDistribution.all_distributions.get(name)
            if not distribution:
                distribution = FeatureDistribution(row["type"], name)
            distribution.add_option(row["option"], row["weight"])

    def add_option(self, option, weight):
        if option in self.weights:
            self.total -= self.weights[option]
        weight_value = float(weight)
        self.weights[option] = weight_value
        self.total += weight_value

    def select_random_value(self):
        target_weight = random() * self.total
        for option, weight in self.weights.items():
            if target_weight <= weight:
                return option
            target_weight -= weight
        return None


name = FeatureDistribution(NAME_TYPE, "name")
file = open("distributions.csv")
FeatureDistribution.load_distributions(file)
file.close()


def feature_value(feature, data):
    if data:
        return data.get(feature.name)
    return feature.select_random_value()
