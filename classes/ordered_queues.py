from collections import OrderedDict
from classes.event import Event
from classes.option_spec import OptionSpec
from classes.queue import (
    Queue,
    extended_queue,
)
from classes.specific_feature import SpecificFeature
from classes.universal_feature import UniversalFeature


SPECIFIC_QUEUE = "specific"
UNIVERSAL_QUEUE = "universal"


class OrderedQueues(object):
    name = "ordered_queues"

    features = [SpecificFeature("industry"),
                SpecificFeature("program"),
                UniversalFeature("role",
                                 option_specs=[OptionSpec("Executive", 2),
                                               OptionSpec("Investor"),
                                               OptionSpec("Lawyer")]),
                UniversalFeature("gender", option_specs=[OptionSpec("female"),
                                                         OptionSpec("male")])]
    expected_reads = 4
    startup_needs = {}

    def __init__(self):
        self.queues = []

    def setup(self, judges, startups):
        feature_options = OrderedDict([
                (feature.field, feature.initial_options(judges, startups))
                for feature in OrderedQueues.features])
        self.add_queues(feature_options)
        self.queues.append(Queue(count=OrderedQueues.expected_reads))
        self.add_startups(startups)

    def add_queues(self, slots):
        # slots is an OrderDicts of possible options for each feature
        # e.g., {"industry": ["social-impact", "clean energy",...]}
        for field, slot in slots.items():
            self.add_queues_for_slot(field, slot)

    def add_queues_for_slot(self, field, slot):
        higher_queues = []
        lower_queues = []
        for option in slot:
            field_option = {field: option}
            lower_queues.append(Queue(field_option))
            for queue in self.queues:
                higher_queues.append(extended_queue(queue, field_option))
        self.queues = higher_queues + self.queues + lower_queues

    def add_startups(self, startups):
        # Note: This is O(|startups| * |self.queues|).  We could speed this
        # up to something like
        # O(|startups|*log(|self.queues|) + |self.queues|) with a faster
        # (but more complicated) queue lookup method.
        for startup in startups:
            for queue in self.queues:
                queue.add_if_matches(startup)

    def work_left(self):
        for queue in self.queues:
            if len(queue.items) > 0:
                return True
        return False

    def process_judge_events(self, events):
        for event in events:
            action = event.fields["action"]
            judge = event.fields["subject"]
            startup = event.fields["object"]
            for queue in self.queues:
                queue.process_action(action, judge, startup)
            self.update_needs(action, judge, startup)

    def update_needs(self, action, judge, startup):
        needs = OrderedQueues.startup_needs.get(startup,
                                                self.initial_needs(startup))
        new_needs = {}
        for field, option_counts in needs.items():
            new_option_counts = calc_option_counts(field, option_counts, judge)
            if new_option_counts:
                new_needs[field] = new_option_counts
        OrderedQueues.startup_needs[startup] = new_needs

    def initial_needs(self, startup):
        needs = {}
        for feature in OrderedQueues.features:
            needs[feature.field] = feature.option_counts(startup)
        return needs

    def find_one_startup(self, judge):
        for queue in self.queues:
            startup = queue.next_item(judge)
            if startup:
                return startup
        return None

    def assess(self):
        for queue in self.queues:
            remaining = len(queue.items)
            if remaining > 0:
                Event(action="fail",
                      subject=queue,
                      description="{} item(s) left".format(remaining))
            else:
                Event(action="complete",
                      subject=queue)


def calc_option_counts(field, option_counts, judge):
    result = []
    for option, count in option_counts:
        if judge.properties.get(field, None) == option:
            count = count - 1
        if count > 0:
            result.append((option, count))
    return result
