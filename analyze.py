from app_allocator.classes.allocation_analyzer import AllocationAnalyzer
from sys import argv

def set_up_allocator(scenario='example.csv',
                allocation='tmp.out',
                criteria="criteria.csv"):
    aa = AllocationAnalyzer()
    aa.process_scenario_from_csv(scenario)
    aa.process_allocations_from_csv(allocation)
    criteria_file = open(criteria)
    aa.read_criteria(criteria_file)
    return aa


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

aa = set_up_allocator(scenario, allocation, criteria)
print ("Assigned: ")
print (aa.summarize(aa.assigned))
print ("Completed: ")
print (aa.summarize(aa.completed))

print()
