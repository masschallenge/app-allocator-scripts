# Script for allocation a set of input judges to a set of input startups.
# Syntax:
# python3 allocate.py <csv-file>
# CSV file should be as created by generate.py

# TODO: Output should be as a CSV that can then assessed by a new assess.py
# script.
import sys

from classes.allocator import (
    Allocator,
)
from classes.event import Event


filename = None
heuristic = ""

if len(sys.argv) > 1:
    filepath = sys.argv[1]
if len(sys.argv) > 2:
    heuristic = sys.argv[2]


allocator = Allocator(filepath, heuristic)
allocator.read_entities()
allocator.setup()
allocator.allocate()
allocator.assess()

for event in Event.all_events:
    print (event.to_csv())
