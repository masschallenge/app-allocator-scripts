import mock

from app_allocator.classes.dynamic_matrix_heuristic import (
    DynamicMatrixHeuristic,
    ASSIGNED_VALUE,
    FINISHED_VALUE,
)
from app_allocator.classes.event import Event
from app_allocator.tests.utils import (
    allocator_getter,
    DUMMY_FILEPATH,
    lazy_judge_scenario_csv,
    multiple_application_scenario_csv,
)

_allocator = allocator_getter(DynamicMatrixHeuristic.name)


class TestDynamicMatrixHeuristic(object):
    def test_work_left(self):
        allocator = _allocator()
        assert allocator.heuristic.work_left()

    def test_no_work_left(self):
        allocator = _allocator(applications=[])
        assert not allocator.heuristic.work_left()

    @mock.patch('app_allocator.classes.allocator.Allocator._entity_file',
                multiple_application_scenario_csv)
    def test_find_n_applications(self):
        allocator = _allocator(entity_path=DUMMY_FILEPATH)
        judge = allocator.heuristic.judges[0]
        judge.request_batch(allocator.heuristic)
        assignments = allocator.heuristic.judge_assignments[judge]
        applications = allocator.heuristic.applications
        assert all([app in assignments for app in applications])

    @mock.patch('app_allocator.classes.allocator.Allocator._entity_file',
                lazy_judge_scenario_csv)
    def test_find_n_applications_respects_judge_capacity(self):
        allocator = _allocator(entity_path=DUMMY_FILEPATH)
        judge = allocator.judges[0]
        batch = judge.request_batch(allocator.heuristic)
        assert len(batch) == int(judge['commitment'])

    def test_process_assigned_judge_event_updates_judge_assignments(self):
        application, judge, allocator = self._process_judge_event("assigned")
        assert application in allocator.heuristic.judge_assignments[judge]

    def test_process_assigned_judge_event_updates_app_needs(self):
        application, judge, allocator = self._process_judge_event("assigned")
        _assert_needs(application, judge, allocator, ASSIGNED_VALUE)

    def test_process_finished_judge_event_updates_app_needs(self):
        application, judge, allocator = self._process_judge_event("finished")
        _assert_needs(application, judge, allocator, FINISHED_VALUE)

    def test_process_pass_judge_event_does_not_change_app_needs(self):
        application, judge, allocator = self._process_judge_event("pass")
        _assert_needs(application, judge, allocator, 0)

    def _process_judge_event(self, action):
        allocator = _allocator()
        heuristic = allocator.heuristic
        judge = heuristic.judges[0]
        application = heuristic.applications[0]
        heuristic.process_judge_events(
            [Event(action=action,
                   subject=judge,
                   object=application)])
        return application, judge, allocator


def _assert_needs(application, judge, allocator, adjustment):
    heuristic = allocator.heuristic
    needs_dict = heuristic.application_needs[application]
    for criterion, option in judge.properties.items():
        key = (criterion, option)
        if key in needs_dict:
            initial_value = _initial_value(heuristic,
                                           key,
                                           application)
            assert needs_dict[key] == initial_value - adjustment


def _initial_value(heuristic, key, application):
    return heuristic.initial_application_needs()[application][key]
