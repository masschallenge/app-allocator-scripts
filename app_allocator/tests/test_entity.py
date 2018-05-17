from app_allocator.classes.entity import (
    csv_output,
    Entity,
)
from app_allocator.classes.feature_distribution import (
    MATCHING_TYPE,
    FeatureDistribution,
)
from app_allocator.tests.utils import assert_only_these_fields_in_csv_row


test_feature_distribution = FeatureDistribution(MATCHING_TYPE, 'color')
test_feature_distribution.add_option("blue", 1.0)


class TestEntity(object):
    def test_str_name_exists(self):
        entity = Entity()
        name = "Joe Smith"
        entity.properties['name'] = name
        assert str(entity) == name

    def test_str_no_name_exists(self):
        entity = Entity()
        assert str(entity) == "%s %d" % (entity.type, entity.id())

    def test_csv_no_values_set(self):
        entity = Entity()
        fields = [str(entity),
                  entity.type]
        assert_only_these_fields_in_csv_row(fields, entity.csv())

    def test_getitem(self):
        entity = Entity(dists=[test_feature_distribution])
        assert entity['color'] == 'blue'

    def test_csv_output(self, capsys):
        entity = Entity()
        entity.add_property(test_feature_distribution)
        csv_output([entity])
        captured, _ = capsys.readouterr()
        line = captured.split("\n")[1]
        fields = [str(entity),
                  entity.type]
        assert_only_these_fields_in_csv_row(fields, line)
