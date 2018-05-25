from app_allocator.classes.criterion import (
    DEFAULT_COUNT,
    DEFAULT_WEIGHT,
)
from app_allocator.classes.reads_criterion import ReadsCriterion


class TestReadsCriterion(object):
    def test_criterion_with_option_specs(self):
        criterion = ReadsCriterion("reads")
        expected_count = 4 * DEFAULT_COUNT
        expected_weight = 2 * DEFAULT_WEIGHT
        criterion.add_option(option="reads",
                             count=expected_count,
                             weight=expected_weight)
        assert criterion.count == expected_count
        assert criterion.weight == expected_weight
