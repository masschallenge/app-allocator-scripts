from app_allocator.classes.read_need import ReadNeed


class ReadsFeature(object):
    def __init__(self, count):
        self.count = count

    def setup(self, judges, applications):
        pass

    def as_need(self, application):
        return ReadNeed(count=self.count)
