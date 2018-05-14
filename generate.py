# Generates a set of random judges and applications per the distributions
# given in app_allocator.classes.feature_distribution.  Syntax:
# python3 generate.py <judge-count> <application-count>
import sys
from app_allocator.classes.entity import csv_output
from app_allocator.classes.generator import Generator
from app_allocator.classes.feature_distribution import FeatureDistribution


file = open("distributions.csv")
FeatureDistribution.load_distributions(file)
file.close()

generator = Generator(judge_count=int(sys.argv[1]),
                      application_count=int(sys.argv[2]))


csv_output(generator.judges + generator.applications)
