# Script for allocation a set of input judges to a set of input startups.
# Syntax:
# python3 allocate.py <csv-file>
# CSV file should be as created by generate.py

# TODO: Output should be as a CSV that can then assessed by a new assess.py
# script.
import csv
import sys
from random import choice

from classes.allocator import Allocator
from classes.bin import BIN_DEFAULT_WEIGHT
from classes.female_bin import FemaleBin
from classes.home_program_bin import HomeProgramBin
from classes.industry_bin import IndustryBin
from classes.judge import Judge
from classes.property import program
from classes.property import industry
from classes.reads_bin import ReadsBin
from classes.role_bin import RoleBin
from classes.satisfied_bin import SatisfiedBin
from classes.startup import Startup


if len(sys.argv) > 1:
    filepath = sys.argv[1]
else:
    filepath = None
    

allocator = Allocator(filepath)
allocator.read_entities()
allocator.default_bins()
allocator.add_startups()
allocator.calc_capacity()
allocator.allocate()
allocator.assess_allocations()
allocator.assess_bins()
