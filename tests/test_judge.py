from app_allocator_scripts.classes.judge import Judge
from app_allocator_scripts.classes.event import Event


class TestJudge(object):
    def test_judge_mark_as_done_creates_event(self):
        judge = Judge()
        prior_ticks = Event.ticks
        judge.mark_as_done()
        assert Event.ticks == prior_ticks + 1
        assert Event.all_events[-1].fields['subject'] == judge
