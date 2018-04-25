from app_allocator.classes.event import Event
from app_allocator.tests.utils import assert_only_these_fields_in_csv_row

event_fields = {'a': 'bcdef', 'b': 'cdefghi'}


class TestEvent(object):
    def test_event_to_csv(self):
        event = Event(**event_fields)
        csv_fields = event.to_csv().split(",")
        assert all([field in csv_fields for field in event_fields.values()])

    def test_update_event_existing_field(self):
        event = Event(**event_fields)
        value = 'tuvwxy'
        event.update(**{'b': value})
        assert event.fields['b'] == value

    def test_update_event_new_field(self):
        event = Event(**event_fields)
        value = 'tuvwxy'
        event.update(**{'c': value})
        assert event.fields['c'] == value

    def test_header_row(self):
        event = Event(**event_fields)
        event.update(**{'q': 'prstuv'})
        assert_only_these_fields_in_csv_row(Event.headers, Event.header_row())

    def test_all_events_as_csv(self):
        Event.all_events = []
        event = Event(**event_fields)
        rows = Event.all_events_as_csv().split("\n")
        assert_only_these_fields_in_csv_row(event.fields.values(), rows[1])
