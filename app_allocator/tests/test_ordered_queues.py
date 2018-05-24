import mock

from app_allocator.classes.event import Event
from app_allocator.classes.ordered_queues import OrderedQueues
from app_allocator.tests.utils import (
    DUMMY_FILEPATH,
    allocator_getter,
    satisfiable_scenario_csv,
    simple_test_scenario_csv,
)


_allocator = allocator_getter(OrderedQueues.name)


def _finished_allocator():
    allocator = _allocator()
    for queue in allocator.heuristic.queues:
        queue.items = []
    return allocator


class TestOrderedQueues(object):
    def test_work_left(self):
        allocator = _allocator()
        assert allocator.heuristic.work_left()

    def test_queue_str(self):
        allocator = _allocator()
        queue = allocator.heuristic.queues[0]
        assert(all([str(need) in str(queue) for need in queue.needs]))

    def test_needs_eq(self):
        allocator = _allocator()
        app = allocator.applications[0]
        needs = allocator.heuristic._initial_needs(app)
        assert needs == allocator.heuristic.application_needs[app]

    def test_no_work_left(self):
        allocator = _allocator(applications=[])
        assert not allocator.heuristic.work_left()

    def test_process_judge_events(self):
        allocator = _allocator()
        heuristic = allocator.heuristic
        heuristic.process_judge_events(
            [Event(action="finished",
                   subject=allocator.judges[0],
                   object=allocator.applications[0])])
        assert heuristic.work_left()

    @mock.patch('app_allocator.classes.allocator.Allocator._entity_file',
                simple_test_scenario_csv)
    def test_run_allocator(self):
        allocator = _allocator(entity_path=DUMMY_FILEPATH)
        allocator.allocate()
        assert allocator.heuristic.work_left()

    @mock.patch('app_allocator.classes.allocator.Allocator._entity_file',
                satisfiable_scenario_csv)
    def test_run_allocator_to_with_no_passes(self):
        allocator = _allocator(entity_path=DUMMY_FILEPATH)
        for judge in allocator.judges:
            judge.chance_of_pass = 0
        allocator.allocate()
        assert not allocator.heuristic.work_left()

    @mock.patch('app_allocator.classes.allocator.Allocator._entity_file',
                satisfiable_scenario_csv)
    def test_run_allocator_to_with_only_passes(self):
        allocator = _allocator(entity_path="some/file/path")
        for judge in allocator.judges:
            judge.chance_of_pass = 1
        allocator.allocate()
        assert not allocator.judges

    def test_find_one_application(self):
        allocator = _allocator()
        judge = allocator.judges[0]
        application = allocator.applications[0]
        assert allocator.heuristic.find_one_application(judge) == application

    def test_no_application(self):
        allocator = _allocator(applications=[])
        judge = allocator.judges[0]
        tmp = allocator.heuristic.find_one_application(judge)
        assert tmp is None

    def test_assess_failure(self):
        self.assess_helper(_allocator(), "fail")

    def test_assess_success(self):
        self.assess_helper(_finished_allocator(), "complete")

    def test_assess_zscore(self):
        self.assess_helper(_finished_allocator(),
                           "final_zscore",
                           zscore_report=True)

    def assess_helper(self, allocator, expected, zscore_report=False):
        event_count = len(Event.all_events)
        allocator.heuristic.assess(zscore_report=zscore_report)
        assert event_count < len(Event.all_events)
        assert any([event.fields["action"] == expected
                    for event in Event.all_events])
