from csv import DictReader
from collections import (
    defaultdict,
    namedtuple,
)
from classes.judge import Judge
from classes.startup import Startup
Assignment = namedtuple("Assignment", ["judge", "startup"])


def increment_assignment_count(startup, metric_name, analysis):
    name = startup['name']
    analysis[name][metric_name] += 1


def female_judge(assignment, read_counts):
    judge, startup = assignment
    if judge.is_female():
        increment_assignment_count(startup, 'female_reads', read_counts)


def role_distribution(assignment, read_counts):
    judge, startup = assignment
    metric_name = "%s_reads" % judge['role']
    increment_assignment_count(startup, metric_name, read_counts)


def program_match(assignment, read_counts):
    judge, startup = assignment
    metric_name = "home_program_reads"
    if startup['program'] == judge['program']:
        increment_assignment_count(startup, metric_name, read_counts)


def industry_match(assignment, read_counts):
    judge, startup = assignment
    metric_name = "matching_industry_reads"
    if startup['industry'] == judge['industry']:
        increment_assignment_count(startup, metric_name, read_counts)


def total_reads(assignment, read_counts):
    _, startup = assignment
    increment_assignment_count(startup, 'total_reads', read_counts)


class AllocationAnalyzer(object):
    def __init__(self):
        self.judges = {}
        self.startups = {}
        self.assigned = []
        self.completed = []
        self.metrics = [total_reads,
                        female_judge,
                        role_distribution,
                        program_match,
                        industry_match]

    def read_scenario_from_csv(self, input_file):
        with open(input_file) as file:
            reader = DictReader(file)
            self.process_scenario_from_csv(reader)

    def read_allocations_from_csv(self, input_file):
        with open(input_file) as file:
            reader = DictReader(file)
            self.process_allocations_from_csv(reader)

    def process_scenario_from_csv(self, reader):
        for row in reader:
            if row['type'] == "judge":
                judge = Judge(data=row)
                self.judges[judge['name']] = judge
            elif row['type'] == "startup":
                startup = Startup(data=row)
                self.startups[startup['name']] = startup
            else:
                print("Couldn't read row: %s" % ",".join(row))

    def process_allocations_from_csv(self, reader):
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
            for metric_fn in self.metrics:
                metric_fn(assignment, read_counts)

        return read_counts

    def summarize(self, read_counts):
        summary = defaultdict(int)
        maxes = defaultdict(int)
        mins = defaultdict(int)
        for app, count_dict in read_counts.items():
            for metric, count in count_dict.items():
                summary[metric] += count
                maxes[metric] = max(maxes[metric], count)
                mins[metric] = max(mins[metric], -count)
        total_applications = len(self.startups)
        total_judges = len(self.judges)
        for metric, count in list(summary.items()):
            summary['average %s' % metric] = count / total_applications
        for metric, val in list(maxes.items()):
            summary['max %s' % metric] = val
        for metric, val in list(mins.items()):
            summary['min %s' % metric] = -val

        summary['total_applications'] = total_applications
        summary['total_judges'] = total_judges
        return summary


def quick_setup():
    aa = AllocationAnalyzer()
    aa.read_scenario_from_csv('example.csv')
    aa.read_allocations_from_csv('tmp.out')
    return aa
