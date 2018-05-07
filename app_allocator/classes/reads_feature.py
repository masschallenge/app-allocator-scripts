from app_allocator.classes.feature import Feature
from app_allocator.classes.read_need import ReadNeed


class ReadsFeature(Feature):
    def __init__(self, name):
        super().__init__(name)

    def as_need(self, application):
        return ReadNeed(count=self.count)
