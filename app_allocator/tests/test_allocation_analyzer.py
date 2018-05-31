from csv import DictReader
from mock import patch
from app_allocator.classes.allocation_analyzer import AllocationAnalyzer
from app_allocator.tests.utils import (
    simple_test_scenario_csv,
    simple_allocation_csv,
    standard_criteria,
)


def fake_open_csv_reader(input_file):
    return DictReader(input_file)


def get_analyzer(scenario=None, allocations=None, criteria=standard_criteria):
    analyzer = AllocationAnalyzer()
    if scenario:
        analyzer.process_scenario_from_csv(scenario)
    if allocations:
        analyzer.process_allocations_from_csv(allocations)
    analyzer.read_criteria(criteria())
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
        application = analyzer.assigned[0].application
        assert application in analyzer.applications.values()

    @patch('app_allocator.classes.allocation_analyzer.open_csv_reader',
           fake_open_csv_reader)
    def test_analyze_simple_allocation_analysis(self):
        analyzer = get_analyzer(scenario=simple_test_scenario_csv(),
                                allocations=simple_allocation_csv())
        analysis = analyzer.analyze(analyzer.assigned)
        assert analysis['reads'][''][3] == 1

    @patch('app_allocator.classes.allocation_analyzer.open_csv_reader',
           fake_open_csv_reader)
    def test_summarize_simple_allocation_analysis(self):
        analyzer = get_analyzer(scenario=simple_test_scenario_csv(),
                                allocations=simple_allocation_csv())
        analysis = analyzer.analyze(analyzer.assigned)
        summary = analyzer.summarize(analyzer.assigned)
        assert "Executive: 1: %d" % analysis['role']['Executive'][1] in summary
