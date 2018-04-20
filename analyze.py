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
for summary, word in [(aa.summarize(aa.analyze(aa.assigned)), "Assigned"),
                      (aa.summarize(aa.analyze(aa.completed)), "Completed")]:
    print("\n%s Application Stats\n------------------\n" % word)
    print("\n".join(["%s: %s" % (key, val)
                     for key, val in summary.items()]))


print()

