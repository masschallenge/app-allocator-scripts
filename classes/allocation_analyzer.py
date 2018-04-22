from csv import DictReader
from collections import (
    defaultdict,
    namedtuple,
)
from classes.judge import Judge
from classes.startup import Startup
from classes.gender_distribution_metric import GenderDistributionMetric
from classes.judge_role_distribution_metric import JudgeRoleDistributionMetric
from classes.program_match_metric import ProgramMatchMetric
from classes.industry_match_metric import IndustryMatchMetric
from classes.total_reads_metric import TotalReadsMetric

Assignment = namedtuple("Assignment", ["judge", "startup"])
TOTAL_READS_TARGET = 5


class AllocationAnalyzer(object):
    def __init__(self):
        self.judges = {}
        self.startups = {}
        self.assigned = []
        self.completed = []
        self.metrics = [ProgramMatchMetric(1),
                        IndustryMatchMetric(1),
                        TotalReadsMetric(TOTAL_READS_TARGET)]
        self.metrics.extend([
            JudgeRoleDistributionMetric('Lawyer', 1),
            JudgeRoleDistributionMetric('Executive', 2),
            JudgeRoleDistributionMetric('Investor', 1),
            JudgeRoleDistributionMetric('Other', 0)])
        self.metrics.extend([
            GenderDistributionMetric('male', 0),
            GenderDistributionMetric('female', 1)])

    def process_scenario_from_csv(self, input_file):
        reader = open_csv_reader(input_file)
        for row in reader:
            if row['type'] == "judge":
                judge = Judge(data=row)
                self.judges[judge['name']] = judge
            elif row['type'] == "startup":
                startup = Startup(data=row)
                self.startups[startup['name']] = startup
            else:
                print("Couldn't read row: %s" % ",".join(row))

    def process_allocations_from_csv(self, input_file):
        reader = open_csv_reader(input_file)
        for row in reader:
            judge = self.judges.get(row['subject'])
            startup = self.startups.get(row['object'])
            if row['action'] == "assigned":
                self.assigned.append(Assignment(judge, startup))

            elif row['action'] == "finished":
                self.completed.append(Assignment(judge, startup))

    def analyze(self, assignments):
        read_counts = {startup['name']: defaultdict(int)
                       for startup in self.startups.values()}
        for assignment in assignments:
            for metric in self.metrics:
                metric.evaluate(assignment, read_counts)

        return read_counts

    def summarize(self, read_counts):
        summary = defaultdict(int)
        maxes = defaultdict(int)
        misses = defaultdict(list)
        total_applications = len(self.startups)
        total_judges = len(self.judges)
        for metric, count in list(summary.items()):
            summary['average %s' % metric] = count / total_applications
        for metric, val in list(maxes.items()):
            summary['max %s' % metric] = val
        for metric in self.metrics:
            summary['total %s' % metric.output_key()] = metric.total
            summary['max %s' % metric.output_key()] = metric.max_count
            missed_count = len(metric.unsatisfied_apps)
            summary['missed %s' % metric.output_key()] = missed_count

        summary['total_applications'] = total_applications
        summary['total_judges'] = total_judges
        return summary


def quick_setup(scenario='example.csv', allocation='tmp.out'):
    aa = AllocationAnalyzer()
    aa.process_scenario_from_csv(scenario)
    aa.process_allocations_from_csv(allocation)
    return aa


def open_csv_reader(input_file):
    file = open(input_file)
    reader = DictReader(file)
    return reader
