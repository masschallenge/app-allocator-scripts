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


def _allocator(entity_path="some/file/path",
               heuristic="linear",
               run_setup=True):
    allocator = Allocator(entity_path=entity_path, heuristic=heuristic)
    allocator.read_entities()
    if run_setup:
        allocator.setup()
    return allocator


def _check_for_entities(entity_list, example):
    assert len(entity_list) == 1
    assert entity_list[0]['name'] == example.name


class TestAllocator(object):

    @mock.patch('app_allocator.classes.allocator.Allocator._entity_file',
                simple_test_scenario_csv)
    def test_read_entities_creates_applications(self):
        _check_for_entities(_allocator(run_setup=False).applications,
                            EXAMPLE_APPLICATION_DATA)

    @mock.patch('app_allocator.classes.allocator.Allocator._entity_file',
                simple_test_scenario_csv)
    def test_read_entities_creates_judges(self):
        _check_for_entities(_allocator(run_setup=False).judges,
                            EXAMPLE_JUDGE_DATA)

    @mock.patch('app_allocator.classes.allocator.Allocator._entity_file',
                simple_test_scenario_csv)
    def test_allocator_setup_calls_heuristic_setup(self):
        allocator = _allocator()
        assert (set(allocator.heuristic.applications) ==
                set(allocator.applications))
        assert set(allocator.heuristic.judges) == set(allocator.judges)

    def allocator_assign_applications_helper(self, expected):
        allocator = _allocator()
        judge = allocator.judges[0]
        allocator.assign_applications(judge)
        assert len(judge.current_applications) == expected

    @mock.patch('app_allocator.classes.allocator.Allocator._entity_file',
                multiple_application_scenario_csv)
    def test_allocator_assign_applications_applications_available(self):
        self.allocator_assign_applications_helper(10)

    @mock.patch('app_allocator.classes.allocator.Allocator._entity_file',
                no_application_scenario_csv)
    def test_allocator_assign_applications_no_applications_available(self):
        self.allocator_assign_applications_helper(0)

    @mock.patch('app_allocator.classes.allocator.Allocator._entity_file',
                multiple_application_scenario_csv)
    def test_allocate_all_judges(self):
        allocator = _allocator()
        allocator.allocate()
        assert len(allocator.judges) == 0

    @mock.patch('app_allocator.classes.allocator.Allocator._entity_file',
                simple_test_scenario_csv)
    def test_linear_assess(self):
        allocator = _allocator(heuristic="linear", run_setup=False)
        event_count = len(Event.all_events)
        allocator.assess()
        assert event_count + 1 == len(Event.all_events)
