from app_allocator.classes.bin import (
    BIN_DEFAULT_WEIGHT,
    Bin,
)


class ReadsBin(Bin):
    def __init__(self, weight=BIN_DEFAULT_WEIGHT, count=1):
        super().__init__(weight=weight)
        self.count = count
        self.counts = {}

    def __str__(self):
        return "Read Bin"

    def add_application(self, application):
        matches = super().add_application(application)
        if matches:
            self.counts[application.id()] = self.count
        return matches

    def update_application(self, application, keep=False):
        if not keep:
            count = self.counts[application.id()]
            if count <= 1:
                super().update_application(application=application, keep=False)
                return
            self.counts[application.id()] = count - 1
        super().update_application(application, True)
