from app_allocator.classes.entity import Entity
from app_allocator.classes.property import (
    industry,
    name,
    program,
)
from app_allocator.classes.utils import expected_average


class Application(Entity):
    def __init__(self, data=None):
        super().__init__()
        self.type = "application"
        self.add_property(name, data)
        self.add_property(industry, data)
        self.add_property(program, data)

    def read_count(self):
        return self.properties.get("read_count", 0)

    def add_read_with_zscore(self, zscore):
        current = self.zscore()
        count = self.read_count()
        new_zscore = expected_average(zscore, current, count)
        self.properties["read_count"] = count + 1
        self.properties["zscore"] = new_zscore
