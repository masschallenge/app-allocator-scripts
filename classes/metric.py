

def true_func(*args):
    return True

def increment_read_count(application, output_key, counts_dict):
    startup_name = application['name']
    counts_dict[startup_name][output_key] += 1

class Metric(object):    
    condition = true_func
    
    def evaluate(self, assignment, counts_dict):
        judge, application = assignment
        if self.condition(judge, application):
            increment_read_count(application,
                                 self.output_key(judge, application),
                                 counts_dict)
        
