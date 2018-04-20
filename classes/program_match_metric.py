from classes.metric import Metric

def home_program_match(judge, application):
    return judge['program'] == application['program']

def home_program_key(judge, application):
    return "Home Program Reads"


class ProgramMatchMetric(Metric):
    output_key = home_program_key
    condition = home_program_match
