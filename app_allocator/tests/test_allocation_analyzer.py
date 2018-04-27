from csv import DictReader
from mock import patch
from app_allocator.classes.allocation_analyzer import AllocationAnalyzer
from app_allocator.tests.utils import (
    simple_test_scenario_csv,
    simple_allocation_csv,
)


def fake_open_csv_reader(input_file):
    return DictReader(input_file)


def get_analyzer(scenario=None, allocations=None):
    analyzer = AllocationAnalyzer()
    if scenario:
        analyzer.process_scenario_from_csv(scenario)
    if allocations:
        analyzer.process_allocations_from_csv(allocations)
    return analyzer


class TestAllocationAnalyzer(object):

    @patch('app_allocator.classes.allocation_analyzer.open_csv_reader',
           fake_open_csv_reader)
    def test_process_scenario_from_csv_creates_judges(self):
        analyzer = get_analyzer(scenario=simple_test_scenario_csv())
        assert len(analyzer.judges) == 1

    @patch('app_allocator.classes.allocation_analyzer.open_csv_reader',
           fake_open_csv_reader)
    def test_process_scenario_from_csv_creates_applications(self):
        analyzer = get_analyzer(scenario=simple_test_scenario_csv())
        assert len(analyzer.applications) == 1

    @patch('app_allocator.classes.allocation_analyzer.open_csv_reader',
           fake_open_csv_reader)
    def test_process_allocations_from_csv_reads_assignments(self):
        analyzer = get_analyzer(scenario=simple_test_scenario_csv(),
                                allocations=simple_allocation_csv())
        assert len(analyzer.assigned) == 1
        assert analyzer.assigned[0].application in analyzer.applications.values()

    @patch('app_allocator.classes.allocation_analyzer.open_csv_reader',
           fake_open_csv_reader)
    def test_analyze_simple_allocation(self):
        analyzer = get_analyzer(scenario=simple_test_scenario_csv(),
                                allocations=simple_allocation_csv())
        application = analyzer.assigned[0].application
        read_counts = analyzer.analyze(analyzer.assigned)
        assert application['name'] in read_counts.keys()

    @patch('app_allocator.classes.allocation_analyzer.open_csv_reader',
           fake_open_csv_reader)
    def test_summarize_simple_allocation_analysis(self):
        analyzer = AllocationAnalyzer()
        analyzer.process_scenario_from_csv(simple_test_scenario_csv())
        analyzer.process_allocations_from_csv(simple_allocation_csv())
        application = analyzer.assigned[0].application
        read_counts = analyzer.analyze(analyzer.assigned)
        summary = analyzer.summarize(read_counts)
        application_counts = read_counts[application['name']]
        assert all([val == summary["total %s" % key]
                    for key, val in application_counts.items()])
