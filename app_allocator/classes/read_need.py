class ReadNeed(object):
    def __init__(self, count):
        self.count = count

    def __str__(self):
        return "R(%s)" % self.count

    def __eq__(self, other):
        if isinstance(other, ReadNeed):
            return self.count == other.count
        return NotImplemented  # pragma: nocover

    def process_action(self, action, judge):
        if action == "finished":
            self.count = max(0, self.count - 1)

    def unsatisfied(self):
        return self.count > 0

    def value_for_judge(self, judge, assignments):
        if self.count > 0:
            count = len(assignments)
            if count <= 2:
                return 1/(count + 1)
        return 0
