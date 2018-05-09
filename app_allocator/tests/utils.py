from collections import namedtuple
from io import StringIO


SCENARIO_HEADERS = ['type',
                    'name',
                    'industry',
                    'program',
                    'role',
                    'gender',
                    'commitment',
                    'completed']

HEADER_ROW = ','.join(SCENARIO_HEADERS)

EntityData = namedtuple("EntityData", SCENARIO_HEADERS)

EXAMPLE_JUDGE_DATA = EntityData('judge',
                                '27-user@example.com',
                                'High Tech',
                                'Boston',
                                'Executive',
                                'female',
                                '10',
                                '10')
FULL_JUDGE_SET = [
    EntityData('judge',
               'high-tech-boston-executive-female',
               'High Tech',
               'Boston',
               'Executive',
               'female',
               '10',
               '10'),
    EntityData('judge',
               'clean-tech-switzerland-executive-male',
               'Energy / Clean Tech',
               'Switzerland',
               'Executive',
               'male',
               '10',
               '10'),
    EntityData('judge',
               'general-israel-lawyer-male',
               'General',
               'Israel',
               'Lawyer',
               'male',
               '10',
               '10'),
    EntityData('judge',
               'healthcare-boston-investor-female',
               'Healthcare / Life Sciences',
               'Boston',
               'Investor',
               'female',
               '10',
               '10'),
    EntityData('judge',
               'social-impact-switzerland-other-male',
               'Social Impact',
               'Switzerland',
               'Other',
               'male',
               '10',
               '10'),
]


FULL_APPLICATION_SET = [
    EntityData('application',
               'Boston Clean Tech App',
               'Energy / Clean Tech',
               'Boston',
               '', '', '', ''),
    EntityData('application',
               'Switzerland General App',
               'General',
               'Switzerland',
               '', '', '', ''),
    EntityData('application',
               'Israel Healthcare App',
               'Healthcare / Life Sciences',
               'Israel',
               '', '', '', ''),
    EntityData('application',
               'Boston High Tech App',
               'High Tech',
               'Boston',
               '', '', '', ''),
    EntityData('application',
               'Switzerland Social Impact App',
               'Social Impact',
               'Switzerland',
               '', '', '', ''),
]


EXAMPLE_APPLICATION_DATA = EntityData('application',
                                      'Organization 4676',
                                      'General',
                                      'Boston',
                                      '',
                                      '',
                                      '',
                                      '')


def pseudofile(header_row=HEADER_ROW, data_rows=[]):
    csv_rows = [','.join(row) for row in data_rows]
    content = "\n".join([header_row] + csv_rows)
    return StringIO(content)


def simple_test_scenario_csv(*args):
    return pseudofile(data_rows=[EXAMPLE_JUDGE_DATA, EXAMPLE_APPLICATION_DATA])


TEN_APPLICATIONS = [EntityData('application',
                               'Application %d' % i,
                               'General',
                               'Boston',
                               '', '', '', '')
                    for i in range(10)]


ALLOCATION_HEADERS = ['time', 'action', 'subject', 'object']
ALLOCATION_HEADER_ROW = ','.join(ALLOCATION_HEADERS)
Allocation = namedtuple('Allocation', ALLOCATION_HEADERS)

SIMPLE_ALLOCATION_DATA = ('0',
                          'assigned',
                          '27-user@example.com',
                          'Organization 4676')


def simple_allocation_csv(*args):
    return pseudofile(header_row=ALLOCATION_HEADER_ROW,
                      data_rows=[SIMPLE_ALLOCATION_DATA])


def multiple_application_scenario_csv(*args):
    return pseudofile(data_rows=[EXAMPLE_JUDGE_DATA] + TEN_APPLICATIONS)


def no_application_scenario_csv(*args):
    return pseudofile(data_rows=[EXAMPLE_JUDGE_DATA])


def satisfiable_scenario_csv(*args):
    return pseudofile(data_rows=FULL_JUDGE_SET + FULL_APPLICATION_SET)


def assert_only_these_fields_in_csv_row(fields, csv_row):
    csv_fields = set(csv_row.split(","))
    fields = [str(field) for field in fields]
    csv_fields.discard("")
    assert len(csv_fields) == len(fields)
    for field in fields:
        assert field in csv_fields
