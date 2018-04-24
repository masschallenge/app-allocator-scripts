# Generates a set of random judges and startups per the distributions
# given in app_allocator.classes.property.  Syntax:
# python3 generate.py <judge-count> <startup-count>
import sys
from app_allocator.classes.entity import csv_output
from app_allocator.classes.generator import Generator


generator = Generator(judge_count=int(sys.argv[1]),
                      startup_count=int(sys.argv[2]))


csv_output(generator.judges + generator.startups)
