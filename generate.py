# Generates a set of random judges and applications per the distributions
# given in app_allocator.classes.property.  Syntax:
# python3 generate.py <judge-count> <application-count>
import sys
from app_allocator.classes.entity import csv_output
from app_allocator.classes.generator import Generator
from app_allocator.classes.property import Property


file = open("distributions.csv")
Property.load_properties(file)
file.close()

generator = Generator(judge_count=int(sys.argv[1]),
                      application_count=int(sys.argv[2]))


csv_output(generator.judges + generator.applications)
