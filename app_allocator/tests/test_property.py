from app_allocator.classes.property import (
    MATCHING_TYPE,
    Property,
    property_value,
)


class TestProperty(object):
    def test_property_value_from_data(self):
        prop = Property(MATCHING_TYPE, "color")
        data = {'color': "Blue"}
        assert property_value(prop, data) == "Blue"
