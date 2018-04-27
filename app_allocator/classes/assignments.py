assignments = {}


def assign(judge, application):
    if application:
        judge.add_application(application)
        judge_assignments = assignments.get(judge.id(), set())
        judge_assignments.add(application.id())
        assignments[judge.id()] = judge_assignments


def has_been_assigned(judge, application):
    id = judge.id()
    return ((id in assignments) and
            (application.id() in assignments.get(id, set())))
