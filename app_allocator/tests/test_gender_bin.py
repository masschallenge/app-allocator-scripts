from app_allocator.classes.gender_bin import GenderBin
from app_allocator.classes.judge import Judge
from app_allocator.classes.startup import Startup

WEIGHT = 23
FEMALE = "female"

class TestGenderBin(object):
    def test_weight(self):
        bin = GenderBin(FEMALE, WEIGHT)
        bin.queue = [Startup()]
        judge = Judge()
        judge.remaining = 10
        judge.properties['gender'] = FEMALE
        assert bin.weight(judge) == WEIGHT
