import mock
from app_allocator.classes.allocator import Allocator
from app_allocator.classes.application import Application
from app_allocator.classes.event import Event
from app_allocator.classes.judge import Judge
from app_allocator.classes.ordered_queues import OrderedQueues
from app_allocator.tests.utils import simple_test_scenario_csv


def _allocator(filepath=None, applications=None, judges=None):
    allocator = Allocator(filepath=filepath, heuristic=OrderedQueues.name)
    if filepath:
        allocator.read_entities()
    allocator.applications = _calc_default(allocator.applications,
                                           applications,
                                           Application)
    allocator.judges = _calc_default(allocator.judges, judges, Judge)
    allocator.setup()
    return allocator


def _calc_default(current, arg, klass):
    if not current and arg is None:
        return [klass()]
    if isinstance(arg, list):
        return arg
    return current


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
        assert(all([need.field in str(queue) for need in queue.needs]))

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

    @mock.patch('app_allocator.classes.allocator.Allocator._file',
                simple_test_scenario_csv)
    def test_run_allocator(self):
        allocator = _allocator(filepath="some/file/path")
        allocator.allocate()
        assert allocator.heuristic.work_left()

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

    def assess_helper(self, allocator, expected):
        event_count = len(Event.all_events)
        allocator.heuristic.assess()
        assert event_count + 1 == len(Event.all_events)
        assert any([event.fields["action"] == expected
                    for event in Event.all_events])
