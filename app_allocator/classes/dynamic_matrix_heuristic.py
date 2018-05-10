from random import choices
from collections import defaultdict, OrderedDict
from numpy import matrix, array
from app_allocator.classes.judge import DEFAULT_CHANCE_OF_PASS
from app_allocator.classes.judge_feature import JudgeFeature
from app_allocator.classes.reads_feature import ReadsFeature
from app_allocator.classes.matching_feature import MatchingFeature
from app_allocator.classes.option_spec import OptionSpec


CHANCE_OF_PASS = DEFAULT_CHANCE_OF_PASS
ASSIGNED_VALUE = 1 - CHANCE_OF_PASS
FINISHED_VALUE = CHANCE_OF_PASS

class DynamicMatrixHeuristic(object):
    BATCH_HEURISTIC = True
    name = "dynamic_matrix"
    features = [MatchingFeature("industry",
                                weight=.6),
                MatchingFeature("program",
                                weight=1),
                JudgeFeature("role",
                             weight=.7,
                             option_specs=[OptionSpec("Executive", 2),
                                           OptionSpec("Investor"),
                                           OptionSpec("Lawyer")]),
                JudgeFeature("gender",
                             weight=1,
                             option_specs=[OptionSpec("female"),
                                           OptionSpec("male")]),
                ReadsFeature(count=4, weight=1)]

    expected_reads = 4

    def setup(self, judges, applications):
        self.judges = tuple(judges)
        for judge in self.judges:
            judge.properties["reads"] = ""
        self.applications = tuple(applications)
        self.feature_values = self._feature_values([judges, applications])
        self._judge_features = {}
        self.feature_weights = self._feature_weights()
        self.judge_assignments = defaultdict(list)

        self.completed_judge_assignments = defaultdict(list)

        self.judge_capacities = self._calc_judge_capacities()
        self.application_needs = self.initial_application_needs()

    def process_judge_events(self, events):
        for event in events:
            action = event.fields.get("action")
            judge = event.fields.get("subject")
            application = event.fields.get("object")
            if action and judge and application:
                self._update_needs(action, judge, application)

    def assess(self):
        pass  # pragma: nocover

    def work_left(self):
        return len(self.applications) > 0

    def _calc_judge_capacities(self):
        return {judge: int(judge['commitment']) for judge in self.judges}

    def find_one_application(self, judge):
        result =  self.request_batch(judge, 1)
        if len(result) > 0:
            return result[0]
        else:
            return None

    def request_batch(self, judge, batch_size):
        available_batch_size = min(batch_size, self.judge_capacities[judge])
        judge_features = self.judge_features(judge)
        needs_array = array([list(row.values()) for _, row in self.application_needs.items()])
        feature_weights_array = array([v for v in self.feature_weights.values()])
        needs_matrix = matrix(needs_array * feature_weights_array)
        application_preferences = judge_features * needs_matrix.transpose()
        apps = self.choose_n_applications(judge, application_preferences, available_batch_size)
        for app in apps:
            self.judge_assignments[judge].append(app)
            self.judge_capacities[judge] -= 1
            self._update_needs("assigned", judge, app)
        return apps

    def choose_n_applications(self, judge, application_preferences, n):
        applications = (array(self.applications)[(-application_preferences).argsort()]).flat
        can_assign_to_judge = self._can_assign_func(judge)
        filtered = [app for app in applications if can_assign_to_judge(app)]
        return filtered[:n]

    def _can_assign_func(self, judge):
        '''returns a function which takes an application and returns True
        if the application can be assigned to the judge.
        Presumably this is where we'll put the z-score logic as well.
        '''
        def can_assign_to_judge(application):
            return application not in self.judge_assignments[judge]

        return can_assign_to_judge

    def _feature_values(self, entity_sets):
        return tuple(set([(feature, entity[feature.field])
                          for entities in entity_sets
                          for entity in entities
                          for feature in self.features]))

    def _feature_weights(self):
        return {(feature.field, value):feature.weight for feature, value in self.feature_values}

    def initial_application_needs(self):
        needs = OrderedDict()

        for application in self.applications:
            row = OrderedDict({(feature.field, value): feature.initial_need(application, value)
                               for feature, value in self.feature_values})

            needs[application] = row
        return needs

    def _update_needs(self, action, judge, application):
        needs_dict = self.application_needs[application]
        if action == "pass":
            return
        if action == "assigned":
            assignments_list = self.judge_assignments[judge]
            adjustment = ASSIGNED_VALUE
        elif action == "finished":
            assignments_list = self.completed_judge_assignments[judge]
            adjustment = FINISHED_VALUE            
        assignments_list.append(application)
        for key, val in judge.properties.items():
            self._update_specific_need(needs_dict, key, val, adjustment)

    def _update_specific_need(self, needs_dict, key, val, adjustment_amount):
        if (key, val) in needs_dict.keys():
            needs_dict[(key, val)] = (
                max(0,
                    needs_dict[(key, val)] - adjustment_amount))
            if needs_dict[(key, val)] == 0:
                self.update_needs_and_features(key, val)
        
    def update_needs_and_features(self, key, val):
        needs = [row[(key, val)] for row in self.application_needs.values()]
        if not any(needs):
            for app in self.application_needs.keys():
                del(self.application_needs[app][(key, val)])
            self.feature_values = tuple([(k, v) for k, v in self.feature_values
                                         if not(k.field == key and v == val)])
            self.feature_weights = self._feature_weights()
            self._judge_features = {}

    def judge_features(self, judge):
        if judge not in self._judge_features:
            row = OrderedDict({feature_value: 0
                               for feature_value in self.feature_values})
            for feature in self.features:
                if (feature, judge[feature.field]) in self.feature_values:
                    row[(feature, judge[feature.field])] = 1
            self._judge_features[judge] = matrix(list(row.values()))
        return self._judge_features[judge]
