from app_allocator.classes.property import property_value

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

    def __init__(self):
        Entity.count += 1
        self.properties = {"id": Entity.count}
        self.type = "entity"

    def __str__(self):
        return self.properties.get(
            "name", "{type} {id}".format(type=self.type, id=self.id()))

    def id(self):
        return self.properties["id"]

    def zscore(self):
        return float(self.properties.get("zscore", 0.0))

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

    def add_property(self, property, data=None):
        value = property_value(property, data)
        if value is not None:
            self.properties[property.name] = value

    def __getitem__(self, key):
        return self.properties.get(key, "")


def csv_output(entities):
    print(CSV_HEADER)
    for entity in entities:
        print(entity.csv())
