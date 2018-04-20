

def true_func(*args):
    return True

def increment_read_count(application, output_key, counts_dict):
    startup_name = application['name']
    counts_dict[startup_name][output_key] += 1

class Metric(object):
    def __init__(self):
        self.condition = true_func
        self.satisfied_apps = set()
    
    def evaluate(self, assignment, counts_dict):
        judge, application = assignment
        if self.condition(judge, application):
            increment_read_count(application,
                                 self.output_key(),
                                 counts_dict)
        if self.satisfied(application, counts_dict):
            self.satisfied_apps.add(application)
        else:
            self.satisfied_apps.discard(application)
            
    def satisfied(self, application, counts_dict):
        return True
