class OptionState(object):
    def __init__(self, option, count):
        self.option = option
        self.count = count
        self.assigned = 0

    def __str__(self):
        return "OptionState(%s, %s, %s)" % (self.option,
                                            self.count,
                                            self.assigned)

    def __eq__(self, other):
        if isinstance(other, OptionState):
            return ((self.option == other.option) and
                    (self.count == other.count) and
                    (self.assigned == other.assigned))
        return NotImplemented

    def process_action(self, action):
        if action == "assign":
            self.assigned += 1
        else:
            if action == "finished":
                self.count -= 1
            self.assigned = max(0, self.assigned - 1)
