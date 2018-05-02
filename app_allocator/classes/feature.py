class Feature(object):
    def __init__(self, field, weight=.5, option_specs=None):
        self.field = field
        self.weight = weight
        self.option_specs = option_specs
