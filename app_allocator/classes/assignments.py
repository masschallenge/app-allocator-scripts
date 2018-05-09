def assign(judge, application):
    if application:
        judge.add_application(application)
        application.assign_judge(judge)


def can_be_assigned(judge, application):
    if application in judge.all_applications:
        return False
    count = application.zscore_count
    if count == 0:
        return True
    expected = application.expected_zscore(judge.zscore())
    return zscore_check(application.estimated_zscore(), expected, count)


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
