from app_allocator.classes.reads_bin import (
    READS_BIN_STRING,
    ReadsBin,
)
from app_allocator.classes.judge import Judge
from app_allocator.classes.startup import Startup

WEIGHT = 23


class TestReadsBin(object):
    def test_str(self):
        bin = ReadsBin(WEIGHT)
        assert str(bin) == READS_BIN_STRING

    def test_add_startup(self):
        bin = ReadsBin(WEIGHT)
        startup = Startup()
        result = bin.add_startup(startup)
        assert result

    def test_update_startup_startup_has_enough_reads(self):
        bin = ReadsBin(WEIGHT)
        startup = Startup()
        bin.add_startup(startup)
        bin.update_startup(startup)
        assert startup not in bin.queue

    def test_update_startup_startup_needs_more_reads(self):
        bin = ReadsBin(WEIGHT, 2)
        startup = Startup()
        bin.add_startup(startup)
        bin.update_startup(startup)
        assert startup in bin.queue
