from app_allocator.classes.assignments import has_been_assigned


BIN_NO_WEIGHT = 0
BIN_LOW_WEIGHT = 0.5
BIN_DEFAULT_WEIGHT = 1
BIN_HIGH_WEIGHT = 100


class Bin(object):
    def __init__(self, weight=BIN_DEFAULT_WEIGHT):
        self._weight = weight
        self.queue = []

    def __str__(self):
        return "Generic Bin"

    def add_application(self, application):
        result = self.match(application)
        if result:
            self.queue.append(application)
        return result

    def calc_capacity(self, judges):
        self.capacity = 0
        for judge in judges:
            if self.weight(judge):
                self.capacity += int(judge.properties["commitment"])

    def match(self, entity):
        return True

    def update(self, judge, application, keep):
        if self.weight(judge):
            self.update_application(application, keep)
            self.capacity = max(1, self.capacity - 1)

    def update_application(self, application, keep=False):
        if application in self.queue:
            self.queue.remove(application)
            if keep:
                self.queue.append(application)

    def work_left(self):
        return len(self.queue) > 0

    def weight(self, judge):
        if self.match(judge) and self.work_left():
            return self._weight

    def adjusted_weight(self, judge):
        w = self.weight(judge)
        if w and self.capacity:
            return w*len(self.queue)/float(self.capacity)
        return None

    def next_application(self, judge):
        for application in self.queue:
            if not has_been_assigned(judge, application):
                return application
