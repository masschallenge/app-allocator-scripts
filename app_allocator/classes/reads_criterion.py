from app_allocator.classes.criterion import Criterion
from app_allocator.classes.read_need import ReadNeed


class ReadsCriterion(Criterion):
    type = "reads"

    def __init__(self, name):
        super().__init__(name)

    def as_need(self, application):
        return ReadNeed(count=self.count)
