import mock

from app_allocator.classes.dynamic_matrix_heuristic import (
    DynamicMatrixHeuristic,
)
from app_allocator.classes.event import Event
from app_allocator.tests.utils import (
    allocator_getter,
    BOS_HIGH_TECH_APP,
    DUMMY_FILEPATH,
    lazy_judge_scenario_csv,
    multiple_application_scenario_csv,
    satisfiable_scenario_csv,
)

_allocator = allocator_getter(DynamicMatrixHeuristic)


class TestDynamicMatrixHeuristic(object):
    def test_work_left(self):
        allocator = _allocator()
        assert allocator.heuristic.work_left()

    def test_no_work_left(self):
        allocator = _allocator(applications=[])
        assert not allocator.heuristic.work_left()

    @mock.patch('app_allocator.classes.allocator.Allocator._file',
                multiple_application_scenario_csv)
    def test_request_batch(self):
        allocator = _allocator(filepath=DUMMY_FILEPATH)
        judge = allocator.heuristic.judges[0]
        judge.request_batch(allocator.heuristic)
        assignments = allocator.heuristic.judge_assignments[judge]
        applications = allocator.heuristic.applications
        assert all([app in assignments for app in applications])

    @mock.patch('app_allocator.classes.allocator.Allocator._file',
                lazy_judge_scenario_csv)
    def test_request_batch_respects_judge_capacity(self):
        allocator = _allocator(filepath=DUMMY_FILEPATH)
        judge = allocator.judges[0]
        batch = judge.request_batch(allocator.heuristic)
        assert len(batch) == int(judge['commitment'])

    @mock.patch('app_allocator.classes.allocator.Allocator._file',
                satisfiable_scenario_csv)
    def test_find_one_application(self):
        allocator = _allocator(filepath=DUMMY_FILEPATH)
        judge = allocator.judges[0]
        app = allocator.heuristic.find_one_application(judge)
        assert app['name'] == BOS_HIGH_TECH_APP

    @mock.patch('app_allocator.classes.allocator.Allocator._file',
                satisfiable_scenario_csv)
    def test_find_one_application_returns_none_if_no_unassigned_apps(self):
        allocator = _allocator(filepath=DUMMY_FILEPATH)
        heuristic = allocator.heuristic
        judge = allocator.judges[0]
        heuristic.judge_assignments[judge] = allocator.applications[:]
        app = allocator.heuristic.find_one_application(judge)
        assert app is None

    def test_process_finished_judge_event_adds_app_to_assignments(self):
        allocator = _allocator()
        heuristic = allocator.heuristic
        judge = heuristic.judges[0]
        application = heuristic.applications[0]
        heuristic.process_judge_events(
            [Event(action="assigned",
                   subject=judge,
                   object=application)])
        assert application in heuristic.judge_assignments[judge]
        assert application in heuristic.completed_judge_assignments[judge]
