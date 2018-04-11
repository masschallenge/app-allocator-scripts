from classes.assignments import has_been_assigned


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

    def status(self):
        if self.queue:
            print("fail,{bin},Queue has {count} applications,".format(
                    bin=self, count=len(self.queue)))
        else:
            print("success,{bin},Is empty,".format(bin=self))

    def add_startup(self, startup):
        result = self.match(startup)
        if result:
            self.queue.append(startup)
        return result

    def calc_capacity(self, judges):
        self.capacity = 0
        for judge in judges:
            if self.weight(judge):
                self.capacity += int(judge.properties["commitment"])

    def match(self, entity):
        return True

    def update(self, judge, startup, keep):
        if self.weight(judge):
            self.update_startup(startup, keep)
            self.capacity = max(1, self.capacity - 1)

    def update_startup(self, startup, keep=False):
        if startup in self.queue:
            self.queue.remove(startup)
            if keep:
                self.queue.append(startup)

    def work_left(self):
        return len(self.queue) > 0

    def weight(self, judge, field=None):
        if self.match(judge) and self.work_left():
            return self._weight

    def adjusted_weight(self, judge):
        w = self.weight(judge)
        if w and self.capacity:
            return w*len(self.queue)/float(self.capacity)
        return None

    def next_startup(self, judge):
        for startup in self.queue:
            if not has_been_assigned(judge, startup):
                return startup
