from app_allocator.classes.feature_distribution import FeatureDistribution


DEFAULT_WEIGHT = 1
LIGHT_WEIGHT = 1


class TestFeatureDistribution(object):
    def test_change_weight(self):
        dist = FeatureDistribution("test", "change")
        dist.add_option("1", DEFAULT_WEIGHT)
        dist.add_option("2", DEFAULT_WEIGHT)
        assert dist.total == (DEFAULT_WEIGHT + DEFAULT_WEIGHT)
        dist.add_option("2", LIGHT_WEIGHT)
        assert dist.total == (DEFAULT_WEIGHT + LIGHT_WEIGHT)

    def test_select_random_value_with_no_weights(self):
        dist = FeatureDistribution("test", "no_weights")
        assert dist.select_random_value() is None
