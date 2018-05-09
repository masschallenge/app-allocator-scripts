from app_allocator.classes.application import Application
from app_allocator.classes.matching_feature import MatchingFeature
from app_allocator.classes.option_spec import OptionSpec


class TestMatchingFeature(object):
    def test_missing_option_state(self):
        feature = MatchingFeature(field="color")
        assert feature.option_states(Application()) == []

    def test_feature_with_option_specs(self):
        feature = MatchingFeature("program",
                                  option_specs=[OptionSpec("Boston", 1)])
        assert feature.option_states(Application({"program": "Boston"}))

    def test_feature_without_option_specs(self):
        feature = MatchingFeature("program")
        assert feature.option_states(Application({"program": "Boston"}))
