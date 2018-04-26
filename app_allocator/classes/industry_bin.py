from app_allocator.classes.bin import (
    BIN_DEFAULT_WEIGHT,
    Bin,
)


class IndustryBin(Bin):

    def __init__(self, value, weight=BIN_DEFAULT_WEIGHT):
        super().__init__(property_name="industry",
                         property_value=value,
                         weight=weight)        
