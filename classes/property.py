from random import random


class Property(object):
    all_properties = []

    def __init__(self, name, values):
        self.name = name
        self.values = values
        Property.all_properties.append(self)


gender = Property("gender", [("female", 0.25),
                             ("male", 1.0)])
industry = Property("industry", [("high-tech", 0.6),
                                 ("social impact", 1.0)])
program = Property("program", [("Boston", 0.6),
                               ("Switzerland", 0.8),
                               ("Israel", 1.0)])
role = Property("role", [("Lawyer", 0.2),
                         ("Investor", 0.4),
                         ("Executive", 0.6),
                         ("Other", 1.0)])
commitment = Property("commitment", [(30, 0.1),
                                     (40, 0.3),
                                     (50, 0.7),
                                     (60, 0.9),
                                     (70, 1.0)])


def property_value(property, data):
    if data:
        return data.get(property.name)
    return random_value(property.values)


def random_value(values):
    v = random()
    for (value, cutoff) in values:
        if v < cutoff:
            return value
