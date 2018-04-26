import mock
from app_allocator.classes.allocator import Allocator
from app_allocator.tests.utils import (
    simple_test_scenario_csv,
    no_startup_scenario_csv,
    multiple_startup_scenario_csv,
    judge_data,
    startup_data,
)


def _allocator(filepath="some/file/path", heuristic="linear"):
        allocator = Allocator("some/file/path", heuristic)
        allocator.read_entities()
        return allocator
    
def _set_up_allocator(filepath="some/file/path", heuristic="linear"):
    allocator = _allocator()
    allocator.setup()
    return allocator


class TestAllocator(object):

    @mock.patch('app_allocator.classes.allocator.Allocator._file',
                simple_test_scenario_csv)
    def test_read_entities_creates_startups(self):
        allocator = _allocator("random")
        assert len(allocator.startups) == 1
        startup = allocator.startups[0]
        assert startup['name'] == startup_data.name

    @mock.patch('app_allocator.classes.allocator.Allocator._file',
                simple_test_scenario_csv)
    def test_read_entities_creates_judges(self):
        allocator = _allocator()
        assert len(allocator.judges) == 1
        judge = allocator.judges[0]
        assert judge['name'] == judge_data.name

    @mock.patch('app_allocator.classes.allocator.Allocator._file',
                simple_test_scenario_csv)
    def test_allocator_setup_calls_heuristic_setup(self):
        allocator = set_up_allocator()
        assert allocator.heuristic.startups == allocator.startups
        assert allocator.heuristic.judges == allocator.judges

    @mock.patch('app_allocator.classes.allocator.Allocator._file',
                multiple_startup_scenario_csv)
    def test_allocator_assign_startups_startups_available(self):
        allocator = set_up_allocator()
        judge = allocator.judges[0]
        allocator.assign_startups(judge)
        assert len(judge.startups) == 10

    @mock.patch('app_allocator.classes.allocator.Allocator._file',
                no_startup_scenario_csv)
    def test_allocator_assign_startups_no_startups_available(self):
        allocator = set_up_allocator()
        judge = allocator.judges[0]
        allocator.assign_startups(judge)
        assert len(judge.startups) == 0

    @mock.patch('app_allocator.classes.allocator.Allocator._file',
                multiple_startup_scenario_csv)
    def test_allocate_all_judges(self):
        allocator = set_up_allocator()
        allocator.allocate()
        assert len(allocator.judges) == 0
