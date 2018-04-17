from classes.entity import Entity
from classes.property import (
    industry,
    name,
    program,
)


class Startup(Entity):
    def __init__(self, data=None):
        super().__init__()
        self.type = "startup"
        self.add_property(name, data)
        self.add_property(industry, data)
        self.add_property(program, data)
        self.add_fields_to_name(["industry", "program"])
