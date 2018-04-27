class Metric(object):
    def __init__(self, target):
        self.target = target
        self.unsatisfied_apps = set()
        self.total = 0
        self.max_count = 0

    def condition(self, judge, application):
        return True

    def evaluate(self, assignment, counts_dict):
        judge, application = assignment
        if self.condition(judge, application):
            self.total += 1
            self.increment_read_count(application,
                                      counts_dict)
        self.update_max(application['name'], counts_dict)
        if self.satisfied(application, counts_dict):
            self.unsatisfied_apps.discard(application)
        else:
            self.unsatisfied_apps.add(application)

    def update_max(self, application_name, counts_dict):
        app_count = counts_dict[application_name][self.output_key()]
        self.max_count = max(self.max_count, app_count)

    def satisfied(self, application, counts_dict):
        app_counts = counts_dict[application['name']]
        return app_counts[self.output_key()] >= self.target

    def increment_read_count(self, application, counts_dict):
        application_name = application['name']
        counts_dict[application_name][self.output_key()] += 1
