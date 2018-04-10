from collections import OrderedDict

class Event(object):
    def __init__(self, **kwargs):
        self.fields= OrderedDict(
            {"time":"", "action":"", "judge":"", "startup":"", "bin":""})
        self.fields.update(kwargs)

    def to_csv(self):
        template = (",".join(["{%s}" % key for key in self.fields.keys()]))
        return template.format(**self.fields)

    def update(self, **kwargs):
        self.__dict__.update(kwargs)
