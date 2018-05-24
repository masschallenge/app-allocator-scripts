from app_allocator.classes.criteria_reader import CriteriaReader
from app_allocator.classes.dynamic_matrix_heuristic import (
    DynamicMatrixHeuristic,
)
from app_allocator.classes.linear_selection import (
    LinearSelection,
)
from app_allocator.classes.ordered_queues import (
    OrderedQueues,
)
from app_allocator.classes.random_selection import (
    RandomSelection,
)
DEFAULT_CRITERIA_PATH = "criteria.csv"

HEURISTICS = [DynamicMatrixHeuristic,
              LinearSelection,
              OrderedQueues,
              RandomSelection]

HEURISTICS_DICT = {heuristic.name: heuristic for heuristic in HEURISTICS}


def find_heuristic(name, criteria_path):
    if not criteria_path:
        criteria_path = DEFAULT_CRITERIA_PATH
    file = open(criteria_path)
    criteria = CriteriaReader(file).all()
    file.close()
    heuristic_instance = HEURISTICS_DICT.get(name, RandomSelection)(criteria)
    return heuristic_instance
