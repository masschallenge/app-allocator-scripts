import mock
from random import random
from app_allocator.classes.judge import Judge
from app_allocator.classes.event import Event
from app_allocator.classes.startup import Startup

def always_pass(*args, **kwargs):
    return True

class TestJudge(object):
    def test_judge_mark_as_done_creates_event(self):
        judge = Judge()
        prior_ticks = Event.ticks
        judge.mark_as_done()
        assert Event.ticks == prior_ticks + 1
        assert Event.all_events[-1].fields['subject'] == judge

    def test_judge_mark_as_done_zeroes_judge_remaining_count(self):
        judge = Judge()
        judge.remaining = 10
        judge.mark_as_done()
        assert judge.remaining == 0

    def test_complete_startups_creates_events_for_all_startups(self):
        judge = Judge()
        startups = [Startup() for _ in range(10)]
        judge.startups = startups[:]
        events = judge.complete_startups()
        event_startups = [event.fields['object'] for event in events]
        assert all([startup in event_startups for startup in startups])

    @mock.patch("app_allocator.classes.judge.Judge.passes", always_pass)
    def test_judge_passes_on_startups(self):
        judge = Judge()
        judge.startups = [Startup() for _ in range(10)]
        judge.complete_startups()
        actions = [event.fields['action'] for event in Event.all_events[-10:]]
        assert all([action=='pass' for action in actions])
        
    def test_needs_another_startup_returns_true_when_startup_needed(self):
        judge = Judge()
        judge.startups = [Startup() for _ in range(Judge.MAX_PANEL_SIZE - 1)]
        judge.remaining = 1
        assert judge.needs_another_startup()

    def test_needs_another_startup_returns_false_when_judge_has_no_capacity(self):
        judge = Judge()
        judge.startups = [Startup() for _ in range(Judge.MAX_PANEL_SIZE - 1)]
        judge.remaining = 0
        assert not judge.needs_another_startup()

    def test_needs_another_startup_returns_false_when_batch_complete(self):
        judge = Judge()
        judge.startups = [Startup() for _ in range(Judge.MAX_PANEL_SIZE)]
        judge.remaining = 10
        assert not judge.needs_another_startup()

    def test_add_startup_creates_event(self):
        judge = Judge()
        startup = Startup()
        prior_ticks = Event.ticks
        judge.add_startup(startup)
        event = Event.all_events[-1]
        assert Event.ticks == prior_ticks + 1
        assert event.fields['object'] == startup
        assert event.fields['action'] == "assigned"
    
