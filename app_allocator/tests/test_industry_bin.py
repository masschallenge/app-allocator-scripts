from app_allocator.classes.industry_bin import IndustryBin
from app_allocator.classes.startup import Startup

WEIGHT = 23
INDUSTRY = "Basket Weaving"
OTHER_INDUSTRY = "Ceramics"


class TestIndustryBin(object):
    def test_str(self):

        bin = IndustryBin(INDUSTRY, WEIGHT)
        assert str(bin) == IndustryBin.name_format.format(INDUSTRY)

    def test_match_startup_matches_bin(self):
        bin = IndustryBin(INDUSTRY, WEIGHT)
        startup = Startup()
        startup.properties['industry'] = INDUSTRY
        assert bin.match(startup)

    def test_match_startup_does_not_match_bin(self):
        bin = IndustryBin(INDUSTRY, WEIGHT)
        startup = Startup()
        startup.properties['industry'] = OTHER_INDUSTRY
        assert not bin.match(startup)
