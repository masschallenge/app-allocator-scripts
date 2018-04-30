from app_allocator.classes.event import Event
from app_allocator.classes.field_need import FieldNeed
from app_allocator.classes.judge_feature import JudgeFeature
from app_allocator.classes.matching_feature import MatchingFeature
from app_allocator.classes.option_spec import OptionSpec
from app_allocator.classes.queue import Queue


MATCHING_QUEUE = "matching"
JUDGE_QUEUE = "judge"


class OrderedQueues(object):
    name = "ordered_queues"

    features = [MatchingFeature("industry"),
                MatchingFeature("program"),
                JudgeFeature("role",
                             option_specs=[OptionSpec("Executive", 2),
                                           OptionSpec("Investor"),
                                           OptionSpec("Lawyer")]),
                JudgeFeature("gender", option_specs=[OptionSpec("female"),
                                                     OptionSpec("male")])]
    expected_reads = 4
    application_needs = {}  # Mapping of Application to lists of FieldNeeds
    relevant_actions = ["finished", "pass"]

    def __init__(self):
        self.queues = []
        self.field_queues = {}
        self.application_queues = {}

    def setup(self, judges, applications):
        for feature in OrderedQueues.features:
            feature.calc_initial_options(judges, applications)
        # TODO: Figure out read queue
        # self.queues.append(Queue(count=OrderedQueues.expected_reads))
        self.add_applications(applications)

    def add_applications(self, applications):
        for application in applications:
            needs = self._initial_needs(application)
            OrderedQueues.application_needs[application] = needs
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
            action = event.fields.get("action")
            judge = event.fields.get("subject")
            application = event.fields.get("object")
            if action and judge and application:
                self._update_needs(action, judge, application)

    def _update_needs(self, action, judge, application):
        if action in OrderedQueues.relevant_actions:
            needs = OrderedQueues.application_needs[application]
            new_needs = _calc_new_needs(needs, action, judge)
            OrderedQueues.application_needs[application] = new_needs
            self._queue_for_needs(application)

    def find_one_application(self, judge):
        queue = self._find_best_queue(judge)
        if queue:
            return self._next_item(queue, judge)
        return None

    def _find_best_queue(self, judge):
        best_queue = None
        best_value = -1
        for queue in self.queues:
            value = queue.judge_value(judge)
            if value and value > best_value:
                best_queue = queue
                best_value = value
        return best_queue

    def _next_item(self, queue, judge):
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


def _calc_new_needs(needs, action, judge):
    result = []
    for field_need in needs:
        field_need.process_action(action, judge)
        if field_need.unsatisfied():
            result.append(field_need)
    return result
