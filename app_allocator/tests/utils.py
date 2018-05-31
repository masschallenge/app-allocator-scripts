from collections import namedtuple
from io import StringIO

from app_allocator.classes.allocator import Allocator
from app_allocator.classes.application import Application
from app_allocator.classes.judge import Judge

DUMMY_FILEPATH = "some/file/path"
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

LAZY_JUDGE_DATA = EntityData('judge',
                             '27-user@example.com',
                             'High Tech',
                             'Boston',
                             'Executive',
                             'female',
                             '1',
                             '1')

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


BOS_HIGH_TECH_APP = 'Boston High Tech App'
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
               BOS_HIGH_TECH_APP,
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


def lazy_judge_scenario_csv(*args):
    return pseudofile(data_rows=[LAZY_JUDGE_DATA] + FULL_APPLICATION_SET)


def standard_criteria(*args):
    return pseudofile("\n".join(["type,name,count,weight,option",
                                 "reads,reads,4,1,",
                                 "matching,industry,1,1,",
                                 "matching,program,1,1,",
                                 "judge,role,2,1,Executive",
                                 "judge,role,1,1,Investor",
                                 "judge,role,1,1,Lawyer",
                                 "judge,gender,1,1,female",
                                 "judge,gender,1,1,male"]))


def assert_only_these_fields_in_csv_row(fields, csv_row):
    csv_fields = set(csv_row.split(","))
    fields = [str(field) for field in fields]
    csv_fields.discard("")
    assert len(csv_fields) == len(fields)
    for field in fields:
        assert field in csv_fields


def allocator_getter(heuristic):
    def _allocator(entity_path=None, applications=None, judges=None):

        allocator = Allocator(entity_path=entity_path, heuristic=heuristic)
        if entity_path:
            allocator.read_entities()
        allocator.applications = _calc_default(allocator.applications,
                                               applications,
                                               Application)
        allocator.judges = _calc_default(allocator.judges, judges, Judge)
        allocator.setup()
        return allocator
    return _allocator


def _calc_default(current, arg, klass):
    if not current and arg is None:
        return [klass()]
    if isinstance(arg, list):
        return arg
    return current
