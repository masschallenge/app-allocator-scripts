from collections import OrderedDict


class Event(object):
    all_events = []
    ticks = 0

    def __init__(self, **kwargs):
        self.fields = OrderedDict({"time": Event.ticks,
                                   "action": "",
                                   "subject": "",
                                   "object": "",
                                   "description": ""})
        Event.ticks += 1
        self.fields.update(kwargs)
        Event.all_events.append(self)

    def to_csv(self):
        template = (",".join(["{%s}" % key for key in self.fields.keys()]))
        return template.format(**self.fields)

    def update(self, **kwargs):
        self.fields.update(kwargs)
