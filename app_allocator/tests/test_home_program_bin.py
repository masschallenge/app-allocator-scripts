from app_allocator.classes.home_program_bin import HomeProgramBin
from app_allocator.classes.startup import Startup

WEIGHT = 23
PROGRAM = "New Jersey"
OTHER_PROGRAM = "Idaho"
        
class TestHomeProgramBin(object):
    def test_str(self):

        bin = HomeProgramBin(PROGRAM, WEIGHT)
        assert str(bin) == HomeProgramBin.name_format.format(PROGRAM)

    def test_match_startup_matches_bin(self):
        bin = HomeProgramBin(PROGRAM, WEIGHT)        
        startup = Startup()
        startup.properties['program'] = PROGRAM
        assert bin.match(startup)


    def test_match_startup_does_not_match_bin(self):
        bin = HomeProgramBin(PROGRAM, WEIGHT)        
        startup = Startup()
        startup.properties['program'] = OTHER_PROGRAM
        assert not bin.match(startup)
        
