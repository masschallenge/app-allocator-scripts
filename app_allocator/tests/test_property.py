from app_allocator_scripts.classes.property import (
    Property,
    property_value,
)


class TestProperty(object):
    def test_property_value_from_data(self):
        prop = Property("color")
        data = {'color': "Blue"}
        assert property_value(prop, data) == "Blue"
    
