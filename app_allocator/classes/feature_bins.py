from app_allocator.classes.bin import (
    BIN_DEFAULT_WEIGHT,
    BIN_NO_WEIGHT,
)
from app_allocator.classes.event import Event
from app_allocator.classes.female_bin import FemaleBin
from app_allocator.classes.home_program_bin import HomeProgramBin
from app_allocator.classes.industry_bin import IndustryBin
from app_allocator.classes.property import program
from app_allocator.classes.property import industry
from app_allocator.classes.reads_bin import ReadsBin
from app_allocator.classes.role_bin import RoleBin
from app_allocator.classes.satisfied_bin import SatisfiedBin

FEMALE_WEIGHT = 2
ROLE_WEIGHT = 3
HOME_PROGRAM_WEIGHT = 4
JUDGE_ZSCORE_WEIGHT = 5
INDUSTRY_WEIGHT = 2


class FeatureBins(object):
    name = "feature_bins"

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

    def process_judge_events(self, events):
        for event in events:
            for bin in self.bins:
                bin.update(event.fields["subject"],
                           event.fields["object"],
                           event.fields["action"] == "pass")

    def find_one_startup(self, judge):
        startup, best_bin = find_best_bin(self.bins, judge)
        if startup:
            Event(action=best_bin,
                  subject=startup,
                  object=judge,
                  description="{} left".format(len(best_bin.queue)))
            self.update_bins(startup, judge, True)
        return startup

    def assess(self):
        for bin in self.bins:
            bin.status()

    def update_bins(self, startup, judge, keep):
        for bin in self.bins:
            if bin.weight(judge):
                bin.update_startup(startup, keep)


def find_best_bin(bins, judge):
    next_bin = find_next_bin(bins, judge)
    if next_bin:
        next_startup = next_bin.next_startup(judge)
        if next_startup:
            return next_startup, next_bin
        other_bins = [bin for bin in bins if bin != next_bin]
        return find_best_bin(other_bins, judge)
    return None, None


def find_next_bin(bins, judge):
    result = None
    highest_weight = BIN_NO_WEIGHT
    for bin in bins:
        weight = bin.adjusted_weight(judge)
        if weight and weight > highest_weight:
            highest_weight = weight
            result = bin
    return result


def bin_factory(klass, values, weight):
    return [klass(value=value, weight=weight)
            for value in values]
