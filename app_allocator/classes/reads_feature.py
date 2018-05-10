from app_allocator.classes.read_need import ReadNeed


class ReadsFeature(object):
    def __init__(self, count, weight=.5):
        self.count = count
        self.field = "reads"
        self.weight = weight

    def setup(self, judges, applications):
        pass

    def as_need(self, application):
        return ReadNeed(count=self.count)

    def initial_need(self, startup, value):
        return float(self.count)
