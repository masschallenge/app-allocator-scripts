from csv import DictReader
from collections import (
    Counter, 
    defaultdict,
    namedtuple,
)
from app_allocator.classes.judge import Judge
from app_allocator.classes.application import Application
from app_allocator.classes.gender_distribution_metric import (
    GenderDistributionMetric,
)
from app_allocator.classes.judge_role_distribution_metric import (
    JudgeRoleDistributionMetric,
)
from app_allocator.classes.program_match_metric import ProgramMatchMetric
from app_allocator.classes.industry_match_metric import IndustryMatchMetric
from app_allocator.classes.total_reads_metric import TotalReadsMetric

Assignment = namedtuple("Assignment", ["judge", "application"])
TOTAL_READS_TARGET = 4


class AllocationAnalyzer(object):
    def __init__(self):
        self.judges = {}
        self.applications = {}
        self.assigned = []
        self.completed = []
        self.metrics = [TotalReadsMetric(TOTAL_READS_TARGET),
                        IndustryMatchMetric(1),
                        ProgramMatchMetric(1),
                        ]
        self.metrics.extend([
            JudgeRoleDistributionMetric('Lawyer', 1),
            JudgeRoleDistributionMetric('Executive', 2),
            JudgeRoleDistributionMetric('Investor', 1),
            JudgeRoleDistributionMetric('Other', 0)])
        self.metrics.extend([
            GenderDistributionMetric('female', 1),
            GenderDistributionMetric('male', 0)])

    def process_scenario_from_csv(self, input_file):
        reader = open_csv_reader(input_file)
        for row in reader:
            if row['type'] == "judge":
                judge = Judge(data=row)
                self.judges[judge['name']] = judge
            elif row['type'] == "application":
                application = Application(data=row)
                self.applications[application['name']] = application
            else:
                print("Couldn't read row: %s" % ",".join(row))

    def process_allocations_from_csv(self, input_file):
        reader = open_csv_reader(input_file)
        for row in reader:
            judge = self.judges.get(row.get('subject'))
            application = self.applications.get(row.get('object'))
            if row.get('action') == "assigned":
                self.assigned.append(Assignment(judge, application))

            elif row.get('action') == "finished":
                self.completed.append(Assignment(judge, application))

    def analyze(self, assignments):
        for metric in self.metrics:
            metric.total = 0
        read_counts = {application['name']: defaultdict(int)
                       for application in self.applications.values()}
        for assignment in assignments:
            for metric in self.metrics:
                metric.evaluate(assignment, read_counts)
        return read_counts

    def summarize(self, read_counts, prefix=""):
        dupes = self.detect_duplicate_assignments()
        if dupes:
            print ("Duplicate assignments detected!")
            for dupe, count in dupes:
                print ("%s assigned to %s %d times" % (
                    dupe.application,
                    dupe.judge,
                    count))
        summary = defaultdict(int)
        maxes = defaultdict(int)
        total_applications = len(self.applications)
        total_judges = len(self.judges)
        for metric, count in list(summary.items()):
            summary['%s: average %s' % (prefix, metric)] = count / total_applications
        for metric, val in list(maxes.items()):
            summary['%s: max %s' % (prefix, metric)] = val
        for metric in self.metrics:
            summary['%s: total %s' % (prefix, metric.output_key())] = metric.total
            summary['%s: max %s (%s)' % (prefix, metric.output_key(), metric.max_app)] = metric.max_count
            missed_count = len(metric.unsatisfied_apps)
            summary['%s: missed %s' % (prefix, metric.output_key())] = missed_count

        summary['total_applications'] = total_applications
        summary['total_judges'] = total_judges
        return summary

    def detect_duplicate_assignments(self):
        return [(k, v) for k, v in Counter(self.assigned).items() if v > 1]

def quick_setup(scenario='example.csv', allocation='tmp.out'):
    aa = AllocationAnalyzer()
    aa.process_scenario_from_csv(scenario)
    aa.process_allocations_from_csv(allocation)
    return aa


def open_csv_reader(input_file):
    file = open(input_file)
    reader = DictReader(file)
    return reader
