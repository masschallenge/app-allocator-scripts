from collections import namedtuple
from io import StringIO


def assert_only_these_fields_in_csv_row(fields, csv_row):
    csv_fields = set(csv_row.split(","))
    fields = [str(field) for field in fields]
    csv_fields.discard("")
    assert len(csv_fields) == len(fields)
    for field in fields:
        assert field in csv_fields


scenario_headers = ['type',
                    'name',
                    'industry',
                    'program',
                    'role',
                    'gender',
                    'commitment',
                    'completed']

header_row = ','.join(scenario_headers)

EntityData = namedtuple("EntityData", scenario_headers)

judge_data = EntityData('judge',
                        '27-user@example.com',
                        'High Tech',
                        'Boston',
                        'Executive',
                        'female',
                        '10',
                        '10')
startup_data = EntityData('startup',
                          'Organization 4676',
                          'General',
                          'Boston',
                          '',
                          '',
                          '',
                          '')


def pseudofile(header_row=header_row, data_rows=[]):
    csv_rows = [','.join(row) for row in data_rows]
    content = "\n".join([header_row] + csv_rows)
    return StringIO(content)


def simple_test_scenario_csv(*args):
    return pseudofile(data_rows=[judge_data, startup_data])


ten_startups = [EntityData('startup', 'Startup %d' % i, 'General', 'Boston',
                           '', '', '', '')
                for i in range(10)]


def multiple_startup_scenario_csv(*args):
    return pseudofile(data_rows=[judge_data] + ten_startups)


def no_startup_scenario_csv(*args):
    return pseudofile(data_rows=[judge_data])


allocation_headers = ['time', 'action', 'subject', 'object']
allocation_header_row = ','.join(allocation_headers)
Allocation = namedtuple('Allocation', allocation_headers)

simple_allocation_data = ('0',
                          'assigned',
                          '27-user@example.com',
                          'Organization 4676')


def simple_allocation_csv(*args):
    return pseudofile(header_row=allocation_header_row,
                      data_rows=[simple_allocation_data])
