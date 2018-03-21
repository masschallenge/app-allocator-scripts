from classes.property import property_value

CSV_HEADER = "type,industry,program,role,gender"
CSV_FORMAT = "{type},{industry},{program},{role},{gender}"


class Entity(object):
    count = 0

    def __init__(self):
        Entity.count += 1
        self.properties = { "id": Entity.count }

    def __str__(self):
        return "Entity {}".format(self.id())

    def id(self):
        return self.properties["id"]

    def csv(self):
        return CSV_FORMAT.format(
            type=self.type,
            industry=self.properties.get("industry", ""),
            program=self.properties.get("program", ""),
            role=self.properties.get("role", ""),
            gender=self.properties.get("gender", ""))
            
    def add_property(self, property, data=None):
        value = property_value(property, data)
        self.properties[property.name] = value


def csv_output(entities):
    print(CSV_HEADER)
    for entity in entities:
        print(entity.csv())
