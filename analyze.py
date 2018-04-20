from classes.allocation_analyzer import quick_setup
from sys import stdout

aa = quick_setup()
assigned_summary = aa.summarize(aa.analyze(aa.assigned))
completed_summary = aa.summarize(aa.analyze(aa.completed))

output = ["\nAssigned Application Stats\n------------------\n"]
output.extend("\n".join(["%s: %s" % (key, val) for key, val in assigned_summary.items()]))
output.append("\n\nCompleted Application Stats\n------------------\n")
output.extend("\n".join(["%s: %s" % (key, val) for key, val in completed_summary.items()]))

stdout.writelines(output)



