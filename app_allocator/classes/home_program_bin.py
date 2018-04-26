from app_allocator.classes.bin import (
    BIN_DEFAULT_WEIGHT,
    Bin,
)


class HomeProgramBin(Bin):
    name_format = "{} Home Program Bin"

    def __init__(self, value, weight=BIN_DEFAULT_WEIGHT):
        super().__init__(property_name="program",
                         property_value=value,
                         weight=weight)        
