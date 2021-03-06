# Generates a set of random judges and applications per the distributions
# given in app_allocator.classes.feature_distribution.  Syntax:
# python3 generate.py <judge-count> <application-count>
import sys
from app_allocator.classes.entity import csv_output
from app_allocator.classes.generator import Generator


filename = "distributions.csv"
if len(sys.argv) > 3:
    filename = sys.argv[3]

generator = Generator(filename=filename,
                      judge_count=int(sys.argv[1]),
                      application_count=int(sys.argv[2]))


csv_output(generator.judges + generator.applications)
