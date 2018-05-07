from app_allocator.classes.application import Application
from app_allocator.classes.judge import Judge
from app_allocator.classes.matching_feature import MatchingFeature


class TestMatchingFeature(object):
    def test_missing_option_state(self):
        feature = MatchingFeature(name="color")
        assert feature.option_states(Application()) == []

    def test_feature_with_option_specs(self):
        feature = MatchingFeature("program")
        feature.add_option(option="Boston", count=1)
        assert feature.option_states(Application({"program": "Boston"}))

    def test_feature_without_option_specs(self):
        feature = MatchingFeature("program")
        boston_judge = Judge({"program": "Boston"})
        boston_application = Application({"program": "Boston"})
        feature.setup([boston_judge], [boston_application])
        assert feature.option_states(boston_application)
