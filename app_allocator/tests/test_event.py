from app_allocator.classes.event import Event
from app_allocator.tests.utils import assert_only_these_fields_in_csv_row

EVENT_FIELDS = {'a': 'bcdef', 'b': 'cdefghi'}
VALUE = 'tuvwxy'

class TestEvent(object):
    def test_event_to_csv(self):
        event = Event(**EVENT_FIELDS)
        csv_fields = event.to_csv().split(",")
        assert all([field in csv_fields for field in EVENT_FIELDS.values()])

    def test_update_event_existing_field(self):
        event = Event(**EVENT_FIELDS)
        event.update(**{'b': VALUE})
        assert event.fields['b'] == VALUE

    def test_update_event_new_field(self):
        event = Event(**EVENT_FIELDS)
        event.update(**{'c': VALUE})
        assert event.fields['c'] == VALUE

    def test_header_row(self):
        event = Event(**EVENT_FIELDS)
        event.update(**{'q': VALUE})
        assert_only_these_fields_in_csv_row(Event.headers, Event.header_row())

    def test_all_events_as_csv(self):
        Event.all_events = []
        event = Event(**EVENT_FIELDS)
        rows = Event.all_events_as_csv().split("\n")
        assert_only_these_fields_in_csv_row(event.fields.values(), rows[1])
