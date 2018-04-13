from classes.bin import BIN_DEFAULT_WEIGHT
from classes.reads_bin import ReadsBin


class RoleBin(ReadsBin):
    def __init__(self, value, weight=BIN_DEFAULT_WEIGHT, count=1):
        super().__init__(weight=weight, count=count)
        self.role = value

    def __str__(self):
        return "{} Role Bin".format(self.role)

    def match(self, entity):
        if entity.properties.get("role"):
            return entity.properties["role"] == self.role
        return True

    def update_startup(self, startup, keep=False):
        super().update_startup(startup=startup, keep=keep)
