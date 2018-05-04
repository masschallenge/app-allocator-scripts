from app_allocator.classes.ordered_queues import OrderedQueues
from app_allocator.classes.random_selection import RandomSelection
from app_allocator.classes.linear_selection import LinearSelection
from app_allocator.classes.judge_weighting_heuristic import JudgeWeightingHeuristic
from app_allocator.classes.dynamic_matrix_heuristic import DynamicMatrixHeuristic

HEURISTICS = [RandomSelection,
              LinearSelection,
              OrderedQueues,
              JudgeWeightingHeuristic,
              DynamicMatrixHeuristic]


def find_heuristic(name):
    result = RandomSelection
    options = [heuristic for heuristic in HEURISTICS if heuristic.name == name]
    if options:
        result = options[0]
    return result()
