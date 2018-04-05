assignments = {}


def assign(judge, startup):
    if startup:
        judge.startups.append(startup)
        judge.commitment -= 1
        judge_assignments = assignments.get(judge.id(), set())
        judge_assignments.add(startup.id())
        assignments[judge.id()] = judge_assignments

    
def has_been_assigned(judge, startup):
    id = judge.id()
    return (id in assignments) and (startup.id() in assignments.get(id, set()))
