from classes.bin import Bin


class ReadsBin(Bin):
    def __init__(self, count=5):
        super().__init__()
        self.count = count
        self.counts = {}

    def __str__(self):
        return "Read Bin"

    def add_startup(self, startup):
        matches = super().add_startup(startup)
        if matches:
            self.counts[startup.id()] = self.count
        return matches

    def update_startup(self, startup, keep=False):
        if not keep:
            count = self.counts[startup.id()]
            if count <= 1:
                super().update_startup(startup, False)
                return
            self.counts[startup.id()] = count - 1
        super().update_startup(startup, True)

    def value(self, judge):
        if self.work_left():
            return self.counts[self.queue[0].id()]

    def status(self):
        for startup in self.queue:
            print("fail,Needs {count} reads,{startup},{bin}".format(
                    count=self.counts[startup.id()],
                    startup=startup,
                    bin=self))
        super().status()
