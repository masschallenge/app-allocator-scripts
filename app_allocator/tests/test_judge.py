import mock
from app_allocator.classes.judge import Judge
from app_allocator.classes.event import Event
from app_allocator.classes.application import Application


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

    def test_complete_applications_creates_events_for_all_applications(self):
        judge = Judge()
        applications = [Application() for _ in range(10)]
        judge.applications = list(applications)
        events = judge.complete_applications()
        event_applications = [event.fields['object'] for event in events]
        assert all([application in event_applications for application in applications])

    @mock.patch("app_allocator.classes.judge.Judge.passes", always_pass)
    def test_judge_passes_on_applications(self):
        judge = Judge()
        judge.applications = [Application() for _ in range(10)]
        judge.complete_applications()
        actions = [event.fields['action'] for event in Event.all_events[-10:]]
        assert all([action == 'pass' for action in actions])

    def test_needs_another_application_returns_true_when_application_needed(self):
        judge = Judge()
        judge.applications = [Application() for _ in range(Judge.MAX_PANEL_SIZE - 1)]
        judge.remaining = 1
        assert judge.needs_another_application()

    def test_needs_another_application_false_when_judge_has_no_capacity(self):
        judge = Judge()
        judge.applications = [Application() for _ in range(Judge.MAX_PANEL_SIZE - 1)]
        judge.remaining = 0
        assert not judge.needs_another_application()

    def test_needs_another_application_returns_false_when_batch_complete(self):
        judge = Judge()
        judge.applications = [Application() for _ in range(Judge.MAX_PANEL_SIZE)]
        judge.remaining = 10
        assert not judge.needs_another_application()

    def test_add_application_creates_event(self):
        judge = Judge()
        application = Application()
        prior_ticks = Event.ticks
        judge.add_application(application)
        event = Event.all_events[-1]
        assert Event.ticks == prior_ticks + 1
        assert event.fields['object'] == application
        assert event.fields['action'] == "assigned"
