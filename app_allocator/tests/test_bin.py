from app_allocator.classes.assignments import assign
from app_allocator.classes.bin import (
    Bin,
    BIN_DEFAULT_WEIGHT,
)
from app_allocator.classes.judge import Judge
from app_allocator.classes.startup import Startup


class TestBin(object):
    def test_weight(self):
        bin = Bin()
        bin.queue = [Startup()]
        judge = Judge()
        judge.remaining = 10
        assert bin.weight(judge) == BIN_DEFAULT_WEIGHT

    def test_str(self):
        bin = Bin()
        assert str(bin) == "Generic Bin"

    def test_update(self):
        bin = Bin()
        startup = Startup()
        bin.add_startup(startup)
        judge = Judge()
        bin.calc_capacity([judge])
        prior_capacity = bin.capacity
        bin.update(judge, startup, False)
        assert bin.capacity == prior_capacity - 1

    def test_adjusted_weight(self):
        bin = Bin()
        bin.add_startup(Startup())
        judge = Judge()
        bin.calc_capacity([judge])
        assert bin.adjusted_weight(judge) == bin.weight(judge) / bin.capacity

    def test_adjusted_weight_no_capacity(self):
        bin = Bin()
        bin.add_startup(Startup())
        judge = Judge()
        bin.calc_capacity([])
        assert bin.adjusted_weight(judge) is None

    def test_next_startup(self):
        bin = Bin()
        startup = Startup()
        bin.add_startup(startup)
        judge = Judge()
        assert bin.next_startup(judge) == startup

    def test_next_startup_already_reviewed(self):
        bin = Bin()
        startup = Startup()
        bin.add_startup(startup)
        judge = Judge()
        assign(judge, startup)
        assert bin.next_startup(judge) is None
