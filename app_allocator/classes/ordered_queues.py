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
    application_needs = {}  # Mapping of Application to lists of FieldNeeds

    def __init__(self):
        self.queues = []
        self.field_queues = {}
        self.application_queues = {}

    def setup(self, judges, applications):
        feature_options = OrderedDict([
                (feature.field, feature.initial_options(judges, applications))
                for feature in OrderedQueues.features])
        # self.queues.append(Queue(count=OrderedQueues.expected_reads)) # TODO: Figure out read queue
        self.add_applications(applications)

    def add_applications(self, applications):
        for application in applications:
            OrderedQueues.application_needs[application] = self._initial_needs(application)
            self._queue_for_needs(application)

    def _queue_for_needs(self, application):
        needs = OrderedQueues.application_needs[application]
        self._dequeue(application)
        queue = self._find_queue(needs)
        queue.items.append(application)
        self.application_queues[application] = queue

    def _dequeue(self, application):
        queue = self.application_queues.get(application)
        if queue:
            queue.items.remove(application)

    def _find_queue(self, needs):
        for queue in self.queues:
            if queue.needs == needs:
                return queue
        queue = Queue(needs=needs)
        self.queues.append(queue)
        return queue

    def _initial_needs(self, application):
        needs = []
        for feature in OrderedQueues.features:
            needs.append(FieldNeed(feature.field,
                                   feature.option_states(application)))
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
            application = event.fields["object"]
            self._update_needs(action, judge, application)

    def _update_needs(self, action, judge, application):
        needs = OrderedQueues.application_needs[application]
        new_needs = []
        for field_need in needs:
            field_need.process_action(action, judge)
            if field_need.unsatisfied():
                new_needs.append(field_need)
        OrderedQueues.application_needs[application] = new_needs
        self._queue_for_needs(application)

    def find_one_application(self, judge):
        best_queue = None
        best_value = -1
        application = None
        for queue in self.queues:
            value = queue.judge_value(judge)
            if value and value > best_value:
                best_queue = queue
                best_value = value
        return self._next_item(best_queue, judge)

    def _next_item(self, queue, judge):
        if queue:
            for application in queue.items:
                if queue.assign(judge, application,
                                OrderedQueues.application_needs[application]):
                    self._queue_for_needs(application)
                    return application
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
