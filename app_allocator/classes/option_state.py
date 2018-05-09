class OptionState(object):
    def __init__(self, option, count):
        self.option = option
        self.count = count

    def __str__(self):
        return "O(%s,%s)" % (self.option,
                             self.count)

    def __eq__(self, other):
        if isinstance(other, OptionState):
            return ((self.option == other.option) and
                    (self.count == other.count))
        return NotImplemented  # pragma: nocover

    def process_action(self, action):
        if action == "finished":
            self.count = max(0, self.count - 1)
