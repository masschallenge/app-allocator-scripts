from app_allocator.classes.bin import (
    Bin,
    BIN_DEFAULT_WEIGHT,
)


class GenderBin(Bin):
    def __init__(self, value, weight=BIN_DEFAULT_WEIGHT):
        super().__init__(property_name="gender",
                         property_value=value,
                         weight=weight)        
