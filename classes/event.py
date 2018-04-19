from collections import defaultdict


class Event(object):
    headers = ['time']
    all_events = []
    ticks = 0

    def __init__(self, **kwargs):
        self.fields = defaultdict(str)
        self.fields["time"] = Event.ticks
        Event.ticks += 1
        self.fields.update(kwargs)
        Event.all_events.append(self)
        self.update_headers(kwargs.keys())

    def to_csv(self):
        fields = {field: "" for field in self.headers}
        fields.update(self.fields)
        template = (",".join(["{%s}" % key for key in self.headers]))
        return template.format(**fields)

    def update(self, **kwargs):
        self.fields.update(kwargs)

    @classmethod
    def update_headers(cls, field_names):
        for field_name in field_names:
            if field_name not in cls.headers:
                cls.headers.append(field_name)

    @classmethod
    def header_row(cls):
        return ",".join(cls.headers)

    @classmethod
    def all_events_as_csv(cls):
        result = [cls.header_row()]
        result += [event.to_csv() for event in cls.all_events]
        return "\n".join(result)
