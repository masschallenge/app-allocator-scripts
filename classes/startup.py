from classes.entity import Entity
from classes.property import (
    industry,
    program,
)


class Startup(Entity):
    def __init__(self, data=None):
        super().__init__()
        self.type = "startup"
        self.add_property(industry, data)
        self.add_property(program, data)

    def __str__(self):
        return "Startup {}".format(self.id())

    def update(self, bins, keep):
        for bin in bins:
            bin.update_startup(self, keep)
