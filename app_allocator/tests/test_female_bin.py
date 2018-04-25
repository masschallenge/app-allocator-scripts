from app_allocator.classes.female_bin import (
    FEMALE_BIN_STRING,
    FemaleBin,
)
from app_allocator.classes.judge import Judge
from app_allocator.classes.startup import Startup

WEIGHT = 23


class TestFemaleBin(object):
    def test_weight(self):
        bin = FemaleBin(WEIGHT)
        bin.queue = [Startup()]
        judge = Judge()
        judge.remaining = 10
        judge.properties['gender'] = 'female'
        assert bin.weight(judge) == WEIGHT

    def test_str(self):
        bin = FemaleBin(WEIGHT)
        assert str(bin) == FEMALE_BIN_STRING
