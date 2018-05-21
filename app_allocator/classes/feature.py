class Feature(object):
    all_features = {}

    def __init__(self, type, name):
        self.type = type
        self.name = name
        Feature.all_features[name] = self

    @classmethod
    def find_feature(self, type, name):
        result = Feature.all_features.get(name)
        if result:
            if type != result.type:
                raise TypeError
            return result
        return Feature(type, name)


name_feature = Feature(type="name", name="name")
