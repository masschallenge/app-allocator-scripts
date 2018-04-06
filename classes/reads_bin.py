from classes.bin import Bin


class ReadsBin(Bin):
    def __init__(self, count=4):
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

    def status(self):
        for startup in self.queue:
            print("fail,{bin},{startup},Needs {count} reads".format(
                    count=self.counts[startup.id()],
                    startup=startup,
                    bin=self))
        super().status()
