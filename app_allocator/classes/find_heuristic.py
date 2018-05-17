from app_allocator.classes.dynamic_matrix_heuristic import (
    DynamicMatrixHeuristic,
)
from app_allocator.classes.heuristic import Heuristic
from app_allocator.classes.linear_selection import (
    LinearSelection,
)
from app_allocator.classes.ordered_queues import (
    OrderedQueues,
)
from app_allocator.classes.random_selection import (
    RandomSelection,
)


CURRENT_HEURISTICS = [DynamicMatrixHeuristic,
                      LinearSelection,
                      OrderedQueues,
                      RandomSelection]


for heuristic in CURRENT_HEURISTICS:
    Heuristic.register_heuristic(heuristic)


def find_heuristic(name):
    for heuristic in Heuristic.registered_heuristics:
        if heuristic.name == name:
            return heuristic()
    return Heuristic.registered_heuristics[0]()
