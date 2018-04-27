from app_allocator.classes.ordered_queues import OrderedQueues
from app_allocator.classes.random_selection import RandomSelection
from app_allocator.classes.linear_selection import LinearSelection

HEURISTICS = [RandomSelection, LinearSelection, OrderedQueues]


def find_heuristic(name):
    result = RandomSelection
    options = [heuristic for heuristic in HEURISTICS if heuristic.name == name]
    if options:
        result = options[0]
    return result()
