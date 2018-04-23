from classes.feature_bins import FeatureBins
from classes.ordered_queues import OrderedQueues
from classes.random_selection import RandomSelection

HEURISTICS = [RandomSelection, FeatureBins, OrderedQueues]


def find_heuristic(name):
    result = RandomSelection
    options = [heuristic for heuristic in HEURISTICS if heuristic.name == name]
    if options:
        result = options[0]
    return result()
