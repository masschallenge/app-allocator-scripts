from app_allocator.classes.entity import Entity
from app_allocator.classes.property import (
    industry,
    name,
    program,
)


class Application(Entity):
    def __init__(self, data=None):
        super().__init__()
        self.type = "application"
        self.add_property(name, data)
        self.add_property(industry, data)
        self.add_property(program, data)
