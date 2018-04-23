from app_allocator.classes.satisfied_bin import SatisfiedBin
from app_allocator.classes.judge import Judge
from app_allocator.classes.startup import Startup
from app_allocator.classes.bin import BIN_LOW_WEIGHT


class TestSatisfiedBin(object):
    def test_weight(self):
        bin = SatisfiedBin()
        bin.queue = [Startup()]
        judge = Judge()
        judge.remaining = 10
        assert bin.weight(judge) == BIN_LOW_WEIGHT

    def test_str(self):
        bin = SatisfiedBin()
        assert str(bin) == SatisfiedBin.name_string

    def test_adjusted_weight(self):
        bin = SatisfiedBin()
        judge = Judge()
        bin.calc_capacity([judge])
        assert bin.adjusted_weight(judge) == BIN_LOW_WEIGHT / bin.capacity

    def test_update_startup_always_keeps_startup(self):
        bin = SatisfiedBin()
        judge = Judge()
        startup = Startup()
        bin.add_startup(startup)
        bin.update_startup(startup, keep=False)
        assert startup in bin.queue
