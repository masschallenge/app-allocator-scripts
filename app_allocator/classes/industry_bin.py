from app_allocator.classes.bin import (
    BIN_DEFAULT_WEIGHT,
    Bin,
)


class IndustryBin(Bin):
    name_format = "{} Industry Bin"
    def __init__(self, value, weight=BIN_DEFAULT_WEIGHT):
        super().__init__(weight)
        self.industry = value

    def __str__(self):
        return self.name_format.format(self.industry)

    def match(self, entity):
        return entity.properties["industry"] == self.industry
