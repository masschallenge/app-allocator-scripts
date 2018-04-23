from app_allocator.classes.event import Event


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

    
