from app_allocator.classes.criteria_reader import CriteriaReader
from app_allocator.tests.utils import pseudofile


CRITERIA_HEADER_ROW = ",".join(["type", "name", "count", "weight", "option"])
JUDGE_CRITERION = ("judge", "eye_color", "1", "1", "black")
MATCHING_CRITERION = ("matching", "favorite_color", "1", "1", "")
CONFLICTING_CRITERION = ("judge", "favorite_color", "1", "1", "blue")
READS_CRITERIA = ("reads", "reads", "4", "1", "")


def conflicting_criteria_csv(*args):
    return pseudofile(header_row=CRITERIA_HEADER_ROW,
                      data_rows=[MATCHING_CRITERION, CONFLICTING_CRITERION])


class TestCriteriaReader(object):
    def test_conflict_criteria_reader(self):
        exception_thrown = False
        try:
            CriteriaReader(file=conflicting_criteria_csv())
        except TypeError:
            exception_thrown = True
        assert exception_thrown
