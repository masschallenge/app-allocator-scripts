from csv import DictReader
from random import random


JUDGE_TYPE = "judge"
MATCHING_TYPE = "matching"
NAME_TYPE = "name"
READS_TYPE = "reads"


class Property(object):
    all_properties = {}
    matching_properties = []

    def __init__(self, type, name, values=None):
        self.type = type
        self.name = name
        self.values = values
        self.weights = {}
        self.total = 0
        Property.all_properties[name] = self
        if type == MATCHING_TYPE:
            Property.matching_properties.append(self)

    @classmethod
    def load_properties(self, file):
        reader = DictReader(file)
        for row in reader:
            name = row["name"]
            property = Property.all_properties.get(name)
            if not property:
                property = Property(row["type"], name)
            property.add_option(row["option"], row["weight"])

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


name = Property(NAME_TYPE, "name")
file = open("distributions.csv")
Property.load_properties(file)
file.close()


def property_value(property, data):
    if data:
        return data.get(property.name)
    return property.select_random_value()
