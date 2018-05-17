import mock
from app_allocator.classes.allocator import Allocator
from app_allocator.classes.event import Event
from app_allocator.tests.utils import (
    simple_test_scenario_csv,
    no_application_scenario_csv,
    multiple_application_scenario_csv,
    EXAMPLE_JUDGE_DATA,
    EXAMPLE_APPLICATION_DATA,
)


def _allocator(filepath="some/file/path", heuristic="linear"):
    allocator = Allocator(filepath, heuristic)
    allocator.read_entities()
    return allocator


def set_up_allocator(filepath="some/file/path", heuristic="linear"):
    allocator = _allocator(filepath, heuristic)
    allocator.setup()
    return allocator


class TestAllocator(object):

    @mock.patch('app_allocator.classes.allocator.Allocator._file',
                simple_test_scenario_csv)
    def test_read_entities_creates_applications(self):
        allocator = _allocator()
        assert len(allocator.applications) == 1
        application = allocator.applications[0]
        assert application['name'] == EXAMPLE_APPLICATION_DATA.name

    @mock.patch('app_allocator.classes.allocator.Allocator._file',
                simple_test_scenario_csv)
    def test_read_entities_creates_judges(self):
        allocator = _allocator()
        assert len(allocator.judges) == 1
        judge = allocator.judges[0]
        assert judge['name'] == EXAMPLE_JUDGE_DATA.name

    @mock.patch('app_allocator.classes.allocator.Allocator._file',
                simple_test_scenario_csv)
    def test_allocator_setup_calls_heuristic_setup(self):
        allocator = set_up_allocator()
        assert (set(allocator.heuristic.applications) ==
                set(allocator.applications))
        assert set(allocator.heuristic.judges) == set(allocator.judges)

    def allocator_assign_applications_helper(self, expected):
        allocator = set_up_allocator()
        judge = allocator.judges[0]
        allocator.assign_applications(judge)
        assert len(judge.current_applications) == expected

    @mock.patch('app_allocator.classes.allocator.Allocator._file',
                multiple_application_scenario_csv)
    def test_allocator_assign_applications_applications_available(self):
        self.allocator_assign_applications_helper(10)

    @mock.patch('app_allocator.classes.allocator.Allocator._file',
                no_application_scenario_csv)
    def test_allocator_assign_applications_no_applications_available(self):
        self.allocator_assign_applications_helper(0)

    @mock.patch('app_allocator.classes.allocator.Allocator._file',
                multiple_application_scenario_csv)
    def test_allocate_all_judges(self):
        allocator = set_up_allocator()
        allocator.allocate()
        assert len(allocator.judges) == 0

    @mock.patch('app_allocator.classes.allocator.Allocator._file',
                simple_test_scenario_csv)
    def test_linear_assess(self):
        allocator = _allocator(heuristic="linear")
        event_count = len(Event.all_events)
        allocator.assess()
        assert event_count + 1 == len(Event.all_events)
