assignments = {}


def assign(judge, application):
    if application:
        judge.add_application(application)
        judge_assignments = assignments.get(judge.id(), set())
        judge_assignments.add(application.id())
        assignments[judge.id()] = judge_assignments
