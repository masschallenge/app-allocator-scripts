# Script for allocation a set of input judges to a set of input startups.
# Syntax:
# python3 allocate.py <csv-file>
# CSV file should be as created by generate.py

# TODO: Output should be as a CSV that can then assessed by a new assess.py
# script.
import csv
import sys
from random import choice

from classes.allocator import (
    Allocator,
    RANDOM_SELECTION_HEURISTIC,
)


filename = None
heuristic = RANDOM_SELECTION_HEURISTIC

if len(sys.argv) > 1:
    filepath = sys.argv[1]
if len(sys.argv) > 2:
    heuristic = sys.argv[2]


allocator = Allocator(filepath, heuristic)
allocator.read_entities()
allocator.setup()
allocator.allocate()
allocator.assess()
