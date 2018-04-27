from app_allocator.classes.event import Event
from app_allocator.classes.judge import Judge
from app_allocator.classes.random_selection import RandomSelection
from app_allocator.classes.startup import Startup


def _random_selection():
    result = RandomSelection()
    result.setup([], [Startup()])
    return result


class TestRnadomSelection(object):
    def test_work_left(self):
        heuristic = _random_selection()
        assert heuristic.work_left()

    def test_process_judge_events(self):
        heuristic = _random_selection()
        heuristic.process_judge_events(Event())
        assert heuristic.work_left()

    def test_find_one_startup(self):
        heuristic = _random_selection()
        assert isinstance(heuristic.find_one_startup(Judge()), Startup)

    def test_assess(self):
        event_count = len(Event.all_events)
        _random_selection().assess()
        assert event_count + 1 == len(Event.all_events)
