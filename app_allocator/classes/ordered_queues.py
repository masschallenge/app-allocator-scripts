from collections import OrderedDict
from app_allocator.classes.event import Event
from app_allocator.classes.option_spec import OptionSpec
from app_allocator.classes.queue import (
    Queue,
    extended_queue,
)
from app_allocator.classes.specific_feature import SpecificFeature
from app_allocator.classes.universal_feature import UniversalFeature


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
        self.field_queues = {}

    def setup(self, judges, startups):
        feature_options = OrderedDict([
                (feature.field, feature.initial_options(judges, startups))
                for feature in OrderedQueues.features])
        self.add_queues(feature_options)
        # self.queues.append(Queue(count=OrderedQueues.expected_reads))
        self.add_startups(startups)

    def add_queues(self, slots):
        # slots is an OrderDicts of possible options for each feature
        # e.g., {"industry": ["social-impact", "clean energy",...]}
        for field, slot in slots.items():
            self.add_queues_for_slot(field, slot)

    def add_queues_for_slot(self, field, slot):
        higher_queues = []
        field_options = []
        for option in slot:
            field_options.append((field, option))
            for queue in self.queues:
                higher_queues.append(extended_queue(queue, {field: option}))
        self.queues = higher_queues + self.queues
        self.add_field_option_queues(field_options)

    def add_field_option_queues(self, field_options):
        for field, option in field_options:
            self.add_field_option_queue(field, option)

    def add_field_option_queue(self, field, option):
        queue = Queue(constraints={field: option})
        self.queues.append(queue)
        field_queues = self.field_queues.get(field, {})
        field_queues[option] = queue
        self.field_queues[field] = field_queues
        return queue

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
                self.queue_for_need(startup, field, new_option_counts)
        OrderedQueues.startup_needs[startup] = new_needs

    def queue_for_need(self, startup, field, new_option_counts):
        for option, _ in new_option_counts:
            queue = self.find_queue_for_field_option(field, option)
            if startup not in queue.items:
                queue.items.append(startup)

    def find_queue_for_field_option(self, field, option):
        queues_for_field = self.field_queues.get(field, {})
        if option in queues_for_field:
            return queues_for_field[option]
        return self.add_field_option_queue(field, option)

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
