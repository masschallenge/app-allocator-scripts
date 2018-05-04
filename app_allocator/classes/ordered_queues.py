from random import choice
from app_allocator.classes.event import Event
from app_allocator.classes.judge_feature import JudgeFeature
from app_allocator.classes.matching_feature import MatchingFeature
from app_allocator.classes.needs_queue import NeedsQueue
from app_allocator.classes.option_spec import OptionSpec
from app_allocator.classes.reads_feature import ReadsFeature


class OrderedQueues(object):
    name = "ordered_queues"

    features = [MatchingFeature("industry"),
                MatchingFeature("program"),
                JudgeFeature("role",
                             option_specs=[OptionSpec("Executive", 2),
                                           OptionSpec("Investor"),
                                           OptionSpec("Lawyer")]),
                JudgeFeature("gender", option_specs=[OptionSpec("female"),
                                                     OptionSpec("male")]),
                ReadsFeature(count=4)]
    relevant_actions = ["finished", "pass"]

    def __init__(self):
        self.queues = []
        self.field_queues = {}
        self.application_queues = {}
        self.application_needs = {}

    def setup(self, judges, applications):
        for feature in OrderedQueues.features:
            feature.setup(judges, applications)
        self.add_applications(applications)

    def add_applications(self, applications):
        for application in applications:
            needs = self._initial_needs(application)
            self.application_needs[application] = needs
            self._queue_for_needs(application)

    def _queue_for_needs(self, application, at_front=False):
        needs = self.application_needs[application]
        current_queue = self.application_queues.get(application)
        new_queue = self._find_queue(needs)
        if current_queue and new_queue == current_queue:
            current_queue.move_to_end(application)
        else:
            if current_queue:
                current_queue.remove_application(application)
            if new_queue:
                new_queue.add_application(application, at_front)
            self.application_queues[application] = new_queue

    def _find_queue(self, needs):
        if not needs:
            return None
        for queue in self.queues:
            if queue.needs == needs:
                return queue
        queue = NeedsQueue(needs=needs)
        self.queues.append(queue)
        return queue

    def _initial_needs(self, application):
        return [feature.as_need(application)
                for feature in OrderedQueues.features]

    def work_left(self):
        for queue in self.queues:
            if queue.work_left() > 0:
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
            application.process_judge_action(action, judge)
            needs = self.application_needs[application]
            if needs:
                new_needs = _calc_new_needs(needs, action, judge)
                self.application_needs[application] = new_needs
                self._remove_assignment(application, judge)
                self._queue_for_needs(application, at_front=(action == "pass"))

    def _remove_assignment(self, application, judge):
        queue = self.application_queues[application]
        queue.remove_assignment(application, judge)

    def find_one_application(self, judge):
        queue, value = self._find_best_queue(judge)
        if queue:
            application = self._next_item(queue, judge)
            queue.move_to_end(application)
            Event(action="select", subject=judge, object=application,
                  description="{queue}: {value}".format(queue=str(queue),
                                                        value=value))
            return application
        return None

    def _find_best_queue(self, judge):
        best_queues = []
        best_value = -1
        for queue in self.queues:
            value = queue.judge_value(judge)
            if value:
                if value > best_value:
                    best_queues = [queue]
                    best_value = value
                elif value == best_value:
                    best_queues.append(queue)
        if best_queues:
            return choice(best_queues), best_value
        return None, 0

    def _next_item(self, queue, judge):
        application = queue.assign_next_application(judge)
        return application

    def assess(self):
        for queue in self.queues:
            remaining = queue.remaining()
            if remaining > 0:
                description = "{remaining} item(s) left: {example}".format(
                    remaining=remaining,
                    example=queue.items[0].properties)
                Event(action="fail",
                      subject=queue,
                      description=description)
            else:
                Event(action="complete",
                      subject=queue)
#         self.assess_zscore()

#     def assess_zscore(self):
#         for application in self.application_needs.keys():
#             Event(action="final_zscore", subject=application,
#                   object=application.zscore(),
#                   description=application.read_count())


def _calc_new_needs(needs, action, judge):
    result = []
    for field_need in needs:
        field_need.process_action(action, judge)
        if field_need.unsatisfied():
            result.append(field_need)
    return result
