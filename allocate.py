# Script for allocation a set of input judges to a set of input applications.
# Syntax:
# python3 allocate.py <csv-file>
# CSV file should be as created by generate.py

# TODO: Output should be as a CSV that can then assessed by a new assess.py
# script.
import sys

from app_allocator.classes.allocator import Allocator
from app_allocator.classes.event import Event


criteria_path = None
entity_path = None
heuristic = ""

if len(sys.argv) > 1:
    entity_path = sys.argv[1]
if len(sys.argv) > 2:
    heuristic = sys.argv[2]
if len(sys.argv) > 3:
    criteria_path = sys.argv[3]


allocator = Allocator(criteria_path=criteria_path,
                      entity_path=entity_path,
                      heuristic=heuristic)
allocator.read_entities()
allocator.setup()
allocator.allocate()
allocator.assess()

print(Event.all_events_as_csv())
