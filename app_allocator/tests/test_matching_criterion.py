from app_allocator.classes.application import Application
from app_allocator.classes.judge import Judge
from app_allocator.classes.matching_criterion import MatchingCriterion


class TestMatchingCriterion(object):
    def test_missing_option_state(self):
        # Need to use a unique name due to the registry in
        # Criterion.  Not happy about the persistent state
        # that currently creates, but not ready to redesign.
        criterion = MatchingCriterion(name="animal")
        assert criterion.option_states(Application()) == []

    def test_criterion_with_option_specs(self):
        criterion = MatchingCriterion("program")
        criterion.add_option(option="Boston", count=1)
        assert criterion.option_states(Application({"program": "Boston"}))

    def test_criterion_without_option_specs(self):
        criterion = MatchingCriterion("program")
        boston_judge = Judge({"program": "Boston"})
        boston_application = Application({"program": "Boston"})
        criterion.setup([boston_judge], [boston_application])
        assert criterion.option_states(boston_application)
