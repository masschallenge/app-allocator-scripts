import json
from csv import DictReader
from collections import (
    defaultdict,
    namedtuple,
)
from app_allocator.classes.judge import Judge
from app_allocator.classes.application import Application
from app_allocator.classes.criteria_reader import CriteriaReader

Assignment = namedtuple("Assignment", ["judge", "application"])
TOTAL_READS_TARGET = 4


class AllocationAnalyzer(object):
    def __init__(self):
        self.judges = {}
        self.applications = {}
        self.assigned = []
        self.completed = []
        
    def read_criteria(self, criteria_file):
        self.criteria = CriteriaReader(criteria_file).all()
    
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
        analysis = {}
        for criterion in self.criteria:
            analysis.update(criterion.evaluate(assignments, self.applications))
        return analysis

    def summarize(self, assignments):
        analysis = self.analyze(assignments)
        output_lines = []
        for criterion in self.criteria:
            row = analysis[criterion.name()]
            for option, counts in row.items():
                counts_string = ", ".join([": ".join((str(k), str(v))) for k, v in sorted(counts.items(), reverse=True)])
                
                output_lines.append("%s: %s" % (option or criterion.name(), counts_string))
        return "\n".join(output_lines)

    def to_json(self):
        return json.dumps(self.analyze(self.completed))
    

def quick_setup(scenario='example.csv', allocation='tmp.out', criteria="criteria.csv"):
    aa = AllocationAnalyzer()
    aa.process_scenario_from_csv(scenario)
    aa.process_allocations_from_csv(allocation)
    criteria_file = open(criteria)
    aa.read_criteria(criteria_file)
    return aa


def open_csv_reader(input_file):
    file = open(input_file)
    reader = DictReader(file)
    return reader
