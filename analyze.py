from classes.allocation_analyzer import quick_setup
from sys import (
    argv,
    stdout,
)


if len(argv) > 1:
    scenario = argv[1]
else:
    scenario = "example.csv"
if len(argv) > 2:
    allocation = argv[2]
else:
    allocation = "tmp.out"



aa = quick_setup(scenario, allocation)
assigned_summary = aa.summarize(aa.analyze(aa.assigned))
completed_summary = aa.summarize(aa.analyze(aa.completed))

output = ["\nAssigned Application Stats\n------------------\n"]
output.extend("\n".join(["%s: %s" % (key, val) for key, val in assigned_summary.items()]))
output.append("\n\nCompleted Application Stats\n------------------\n")
output.extend("\n".join(["%s: %s" % (key, val) for key, val in completed_summary.items()]))

stdout.writelines(output)



