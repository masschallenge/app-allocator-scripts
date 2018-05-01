from random import shuffle


class ReadCounter(object):
    def __init__(self, expected_reads):
        self.reads = {}
        self.expected_reads = expected_reads

    def read_value(self, application):
        if self.expected_reads - self.reads.get(application, 0) > 0:
            return 1
        return 0

    def complete_read(self, application):
        self.reads[application] = self.reads.get(application, 0) + 1

    def something_that_needs_a_read(self):
        # Need to stay aware of the assignments
        # Need to think about reads as features
        min_reads = self.expected_reads
        example = None
        candidates = list(self.reads.items())
        shuffle(candidates)
        for app, count in candidates:
            if count < min_reads:
                min_reads = count
                example = app
        return example
