from collections import OrderedDict
from app_allocator.classes.event import Event
from app_allocator.classes.field_need import FieldNeed
from app_allocator.classes.option_spec import OptionSpec
from app_allocator.classes.queue import Queue
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
    startup_needs = {}  # Mapping of Startup to lists of FieldNeeds

    def __init__(self):
        self.queues = []
        self.field_queues = {}
        self.startup_queues = {}

    def setup(self, judges, startups):
        feature_options = OrderedDict([
                (feature.field, feature.initial_options(judges, startups))
                for feature in OrderedQueues.features])
        # self.queues.append(Queue(count=OrderedQueues.expected_reads)) # TODO: Figure out read queue
        self.add_startups(startups)

    def add_startups(self, startups):
        for startup in startups:
            OrderedQueues.startup_needs[startup] = self._initial_needs(startup)
            self._queue_for_needs(startup)

    def _queue_for_needs(self, startup):
        needs = OrderedQueues.startup_needs[startup]
        self._dequeue(startup)
        queue = self._find_queue(needs)
        queue.items.append(startup)
        self.startup_queues[startup] = queue

    def _dequeue(self, startup):
        queue = self.startup_queues.get(startup)
        if queue:
            queue.items.remove(startup)

    def _find_queue(self, needs):
        for queue in self.queues:
            if queue.needs == needs:
                return queue
        queue = Queue(needs=needs)
        self.queues.append(queue)
        return queue

    def _initial_needs(self, startup):
        needs = []
        for feature in OrderedQueues.features:
            needs.append(FieldNeed(feature.field,
                                   feature.option_states(startup)))
        return needs

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
            self._update_needs(action, judge, startup)

    def _update_needs(self, action, judge, startup):
        needs = OrderedQueues.startup_needs[startup]
        new_needs = []
        for field_need in needs:
            field_need.process_action(action, judge)
            if field_need.unsatisfied():
                new_needs.append(field_need)
        OrderedQueues.startup_needs[startup] = new_needs
        self._queue_for_needs(startup)

    def find_one_startup(self, judge):
        best_queue = None
        best_value = -1
        startup = None
        for queue in self.queues:
            value = queue.judge_value(judge)
            if value and value > best_value:
                best_queue = queue
                best_value = value
        return self._next_item(best_queue, judge)

    def _next_item(self, queue, judge):
        if queue:
            for startup in queue.items:
                if queue.assign(judge, startup, OrderedQueues.startup_needs[startup]):
                    self._queue_for_needs(startup)
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
