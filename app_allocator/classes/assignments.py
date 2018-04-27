assignments = {}


def assign(judge, startup):
    if startup:
        judge.add_startup(startup)
        judge_assignments = assignments.get(judge.id(), set())
        judge_assignments.add(startup.id())
        assignments[judge.id()] = judge_assignments
