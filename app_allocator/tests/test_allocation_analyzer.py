from csv import DictReader
from mock import patch
from io import StringIO
from app_allocator.classes.allocation_analyzer import AllocationAnalyzer
from app_allocator.tests.utils import (
    simple_test_scenario_csv,
    simple_allocation_csv,
)


def fake_open_csv_reader(input_file):
    return DictReader(input_file)


class TestAllocationAnalyzer(object):

    @patch('app_allocator.classes.allocation_analyzer.open_csv_reader',
           fake_open_csv_reader)
    def test_process_scenario_from_csv_creates_judges(self):
        analyzer = AllocationAnalyzer()
        analyzer.process_scenario_from_csv(simple_test_scenario_csv())
        assert len(analyzer.judges) == 1

    @patch('app_allocator.classes.allocation_analyzer.open_csv_reader',
           fake_open_csv_reader)
    def test_process_scenario_from_csv_creates_startups(self):
        analyzer = AllocationAnalyzer()
        analyzer.process_scenario_from_csv(simple_test_scenario_csv())
        assert len(analyzer.startups) == 1

    @patch('app_allocator.classes.allocation_analyzer.open_csv_reader',
           fake_open_csv_reader)
    def test_process_allocations_from_csv_reads_assignments(self):
        analyzer = AllocationAnalyzer()
        analyzer.process_scenario_from_csv(simple_test_scenario_csv())
        analyzer.process_allocations_from_csv(simple_allocation_csv())

        assert len(analyzer.assigned) == 1
        assert analyzer.assigned[0].startup in analyzer.startups.values()

    @patch('app_allocator.classes.allocation_analyzer.open_csv_reader',
           fake_open_csv_reader)
    def test_analyze_simple_allocation(self):
        analyzer = AllocationAnalyzer()
        analyzer.process_scenario_from_csv(simple_test_scenario_csv())
        analyzer.process_allocations_from_csv(simple_allocation_csv())

        startup = analyzer.assigned[0].startup
        read_counts = analyzer.analyze(analyzer.assigned)
        assert startup['name'] in read_counts.keys()

    @patch('app_allocator.classes.allocation_analyzer.open_csv_reader',
           fake_open_csv_reader)
    def test_summarize_simple_allocation_analysis(self):
        analyzer = AllocationAnalyzer()
        analyzer.process_scenario_from_csv(simple_test_scenario_csv())
        analyzer.process_allocations_from_csv(simple_allocation_csv())

        startup = analyzer.assigned[0].startup
        read_counts = analyzer.analyze(analyzer.assigned)
        summary = analyzer.summarize(read_counts)
        startup_counts = read_counts[startup['name']]
        assert all([val == summary["total %s" % key]
                    for key, val in startup_counts.items()])
