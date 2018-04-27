from app_allocator.classes.event import Event
from app_allocator.tests.utils import assert_only_these_fields_in_csv_row


EXISTING_FIELD_KEY = 'b'
EVENT_FIELDS = {'a': 'bcdef', EXISTING_FIELD_KEY: 'cdefghi'}
NEW_FIELD_KEY = 'c'
NEW_FIELD_VALUE = 'tuvwxy'


class TestEvent(object):
    def test_event_to_csv(self):
        event = Event(**EVENT_FIELDS)
        csv_fields = event.to_csv().split(",")
        assert all([field in csv_fields for field in EVENT_FIELDS.values()])

    def update_event_helper(self, field):
        event = Event(**EVENT_FIELDS)
        event.update(**{field: NEW_FIELD_VALUE})
        assert event.fields[field] == NEW_FIELD_VALUE

    def test_update_event_existing_field(self):
        self.update_event_helper(EXISTING_FIELD_KEY)

    def test_update_event_new_field(self):
        self.update_event_helper(NEW_FIELD_KEY)

    def test_header_row(self):
        event = Event(**EVENT_FIELDS)
        event.update(**{NEW_FIELD_KEY: NEW_FIELD_VALUE})
        assert_only_these_fields_in_csv_row(Event.headers, Event.header_row())

    def test_all_events_as_csv(self):
        Event.all_events = []
        event = Event(**EVENT_FIELDS)
        rows = Event.all_events_as_csv().split("\n")
        assert_only_these_fields_in_csv_row(event.fields.values(), rows[1])
