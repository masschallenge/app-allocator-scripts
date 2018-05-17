from app_allocator.classes.criteria_reader import CriteriaReader
from app_allocator.classes.ordered_queues import OrderedQueues
from app_allocator.classes.random_selection import RandomSelection
from app_allocator.classes.linear_selection import LinearSelection


HEURISTICS = [RandomSelection, LinearSelection, OrderedQueues]
DEFAULT_CRITERIA_PATH = "criteria.csv"


def find_heuristic(name, criteria_path):
    result = RandomSelection
    if not criteria_path:
        criteria_path = DEFAULT_CRITERIA_PATH
    file = open(criteria_path)
    criteria = CriteriaReader(file).all()
    file.close()
    options = [heuristic for heuristic in HEURISTICS if heuristic.name == name]
    if options:
        result = options[0]
    return result(criteria)
