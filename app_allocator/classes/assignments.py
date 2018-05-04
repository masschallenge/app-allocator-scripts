from app_allocator.classes.utils import expected_average


assignments = {}
application_zscores = {}

DO_ZSCORE_CHECK = True


def assign(judge, application):
    if application:
        judge.add_application(application)
        judge_assignments = assignments.get(judge.id(), set())
        judge_assignments.add(application.id())
        assignments[judge.id()] = judge_assignments


def can_be_assigned(judge, application):
    if has_been_assigned(judge, application):
        return False
    count = application.read_count()
    if count == 0:
        return True
    if DO_ZSCORE_CHECK:
        current = application.zscore()
        expected = expected_average(judge.zscore(), current, count)
        return zscore_check(current, expected, count)
    return True


def has_been_assigned(judge, application):
    id = judge.id()
    return ((id in assignments) and
            (application.id() in assignments.get(id, set())))


def second_read(current, expected):
    return (within_limit(current) or
            (closer_by_half(current, expected) and
             (not signs_differ(current, expected) or within_limit(expected))))


def third_read(current, expected):
    return within_limit(current) or closer_by_half(current, expected)


def fourth_read(current, expected):
    return within_limit(expected)


def additional_reads(current, expected):
    return signs_differ(current, expected)


ABS_ZSCORE_LIMIT = 0.5


def within_limit(value):
    return abs(value) <= ABS_ZSCORE_LIMIT


def signs_differ(a, b):
    return a * b <= 0


def closer_by_half(a, b):
    return abs(a)/2 >= abs(b)


COUNT_ZSCORE_LOOKUP = {
    1: second_read,
    2: third_read,
    3: fourth_read,
}


def zscore_check(current, expected, count):
    count_fn = COUNT_ZSCORE_LOOKUP.get(count, additional_reads)
    return count_fn(current, expected)
