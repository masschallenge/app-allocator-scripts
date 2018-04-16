from classes.bin import BIN_DEFAULT_WEIGHT
from classes.female_bin import FemaleBin
from classes.home_program_bin import HomeProgramBin
from classes.industry_bin import IndustryBin
from classes.property import program
from classes.property import industry
from classes.reads_bin import ReadsBin
from classes.role_bin import RoleBin
from classes.satisfied_bin import SatisfiedBin

FEMALE_WEIGHT = 2
ROLE_WEIGHT = 3
HOME_PROGRAM_WEIGHT = 4
JUDGE_ZSCORE_WEIGHT = 5
INDUSTRY_WEIGHT = 2


class FeatureBins(object):
    def __init__(self):
        self.bins = []

    def setup(self, judges, startups):
        self.default_bins()
        self.add_startups(startups)
        self.calc_capacity(judges)

    def add_startups(self, startups):
        for startup in startups:
            for bin in self.bins:
                bin.add_startup(startup)

    def calc_capacity(self, judges):
        for bin in self.bins:
            bin.calc_capacity(judges)

    def work_left(self):
        return any([bin.work_left() for bin in self.bins])

    def default_bins(self):
        self.bins = (
            [ReadsBin(),
             SatisfiedBin(),
             FemaleBin(weight=FEMALE_WEIGHT*BIN_DEFAULT_WEIGHT),
             RoleBin(value="Executive",
                     weight=ROLE_WEIGHT*BIN_DEFAULT_WEIGHT,
                     count=2),
             RoleBin(value="Lawyer",
                     weight=ROLE_WEIGHT*BIN_DEFAULT_WEIGHT),
             RoleBin(value="Investor",
                     weight=ROLE_WEIGHT*BIN_DEFAULT_WEIGHT)] +
            bin_factory(IndustryBin,
                        values=[value for value, _ in industry.values],
                        weight=INDUSTRY_WEIGHT*BIN_DEFAULT_WEIGHT) +
            bin_factory(HomeProgramBin,
                        values=[value for value, _ in program.values],
                        weight=HOME_PROGRAM_WEIGHT*BIN_DEFAULT_WEIGHT))

    def next_action(self, judge):
        judge.next_action(self.bins)

    def assess(self):
        for bin in self.bins:
            bin.status()


def bin_factory(klass, values, weight):
    return [klass(value=value, weight=weight)
            for value in values]
