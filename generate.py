# Generates a set of random judges and startups per the distributions
# given in classes.property.  Syntax:
# python3 generate.py <judge-count> <startup-count>
import sys
from classes.entity import csv_output
from classes.judge import Judge
from classes.startup import Startup


JUDGE_COUNT = int(sys.argv[1])
judges = [Judge() for i in range(JUDGE_COUNT)]

STARTUP_COUNT = int(sys.argv[2])
startups = [Startup() for i in range(STARTUP_COUNT)]

csv_output(judges + startups)
