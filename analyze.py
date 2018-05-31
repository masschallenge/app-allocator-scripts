from app_allocator.classes.allocation_analyzer import quick_setup
from sys import argv


if len(argv) > 1:
    scenario = argv[1]
else:
    scenario = "example.csv"
if len(argv) > 2:
    allocation = argv[2]
else:
    allocation = "tmp.out"
if len(argv) > 3:
    criteria = argv[3]
else:
    criteria = "criteria.csv"

aa = quick_setup(scenario, allocation, criteria)
print ("Assigned: ")
print (aa.summarize(aa.assigned))
print ("Completed: ")
print (aa.summarize(aa.completed))

print()
