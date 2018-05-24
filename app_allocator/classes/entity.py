CSV_COLUMNS = ["type",
               "name",
               "industry",
               "program",
               "role",
               "gender",
               "commitment",
               "completed",
               "zscore"]
CSV_HEADER = ",".join(CSV_COLUMNS)
CSV_FORMAT = "{%s}" % ("},{".join(CSV_COLUMNS))


class Entity(object):
    count = 0

    def __init__(self, type="entity", data=None, dists=None):
        Entity.count += 1
        self.type = type
        self.properties = {"id": Entity.count}
        if dists:
            self._apply_dists(dists)
        if data:
            self._apply_data(data)

    def __str__(self):
        return self.properties.get(
            "name", "{type} {id}".format(type=self.type, id=self.id()))

    def __repr__(self):
        return str(self)

    def _apply_dists(self, dists):
        for dist in dists:
            self.properties[dist.name()] = dist.select_random_value()

    def _apply_data(self, data):
        for key, value in data.items():
            if value is not '':
                self.properties[key] = value

    def id(self):
        return self.properties["id"]

    def csv(self):
        return CSV_FORMAT.format(
            type=self.type,
            name=str(self),
            industry=self.properties.get("industry", ""),
            program=self.properties.get("program", ""),
            role=self.properties.get("role", ""),
            gender=self.properties.get("gender", ""),
            commitment=self.properties.get("commitment", ""),
            completed=self.properties.get("completed", ""),
            zscore=self.properties.get("zscore", ""))

    def add_property(self, feature, data=None):
        if data:
            value = data.get(feature.name)
            if value is not None:
                self.properties[feature.name] = value

    def __getitem__(self, key):
        return self.properties.get(key, "")


def csv_output(entities):
    print(CSV_HEADER)
    for entity in entities:
        print(entity.csv())
