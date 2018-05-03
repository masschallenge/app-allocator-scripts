from random import random


class Property(object):
    all_properties = []

    def __init__(self, name, values=None):
        self.name = name
        self.values = values
        Property.all_properties.append(self)


name = Property("name")
gender = Property("gender", [("female", 0.25),
                             ("male", 1.0)])

industry = Property("industry", [("Energy / Clean Tech", 0.05),
                                 ("General", 0.40),
                                 ("Healthcare / Life Sciences", 0.56),
                                 ("High Tech", 0.95),
                                 ("Social Impact", 1.0)])
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
completed = Property("completed", [(30, 0.1),
                                   (40, 0.3),
                                   (50, 0.7),
                                   (60, 0.9),
                                   (70, 1.0)])

# Discretized normal distribution
zscore = Property("zscore", [(-2.0, 0.0228),
                             (-1.0, 0.1587),
                             (-0.5, 0.3085),
                             (-0.25, 0.4013),
                             (0.0, 1 - 0.4013),
                             (0.25, 1 - 0.3085),
                             (0.5, 1 - 0.1587),
                             (1.0, 1 - 0.228),
                             (2.0, 1)])


def property_value(property, data):
    if data:
        return data.get(property.name)
    return next_value_below_cutoff(property.values, random())


def next_value_below_cutoff(values, cutoff):
    if values:
        return next((value for value, limit in values if cutoff < limit), None)
    return None
