from app_allocator.classes.feature_distribution import (
    MATCHING_TYPE,
    FeatureDistribution,
    feature_value,
)


class TestFeatureDistribution(object):
    def test_feature_value_from_data(self):
        prop = FeatureDistribution(MATCHING_TYPE, "color")
        data = {'color': "Blue"}
        assert feature_value(prop, data) == "Blue"
