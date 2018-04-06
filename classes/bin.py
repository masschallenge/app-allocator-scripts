from classes.assignments import has_been_assigned


BIN_NO_VALUE = 0
BIN_LOW_VALUE = 0.5
BIN_DEFAULT = 1
BIN_HIGH_VALUE = 100


class Bin(object):
    def __init__(self, value=BIN_DEFAULT):
        self._value = value
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

    def match(self, startup):
        return True

    def update_startup(self, startup, keep=False):
        if startup in self.queue:
            self.queue.remove(startup)
            if keep:
                self.queue.append(startup)

    def work_left(self):
        return len(self.queue) > 0

    def value(self, judge):
        if self.work_left():
            return self._value

    def next_startup(self, judge):
        for startup in self.queue:
            if not has_been_assigned(judge, startup):
                return startup
