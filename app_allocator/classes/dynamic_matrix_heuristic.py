from random import choice
from collections import defaultdict, OrderedDict
from numpy import matrix, array
from app_allocator.classes.judge_feature import JudgeFeature
from app_allocator.classes.reads_feature import ReadsFeature
from app_allocator.classes.matching_feature import MatchingFeature
from app_allocator.classes.option_spec import OptionSpec

REFRESH_TIME = 1000
N = 1

class DynamicMatrixHeuristic(object):
    ticks = 0
    name = "dynamic_matrix"
    features = [MatchingFeature("industry",
                                weight=1.0),
                MatchingFeature("program",
                                weight=1.5),
                JudgeFeature("role",
                             weight=1.0,
                             option_specs=[OptionSpec("Executive", 2),
                                           OptionSpec("Investor"),
                                           OptionSpec("Lawyer")]),
                JudgeFeature("gender",
                             weight=1.5,
                             option_specs=[OptionSpec("female"),
                                           OptionSpec("male")]),
                ReadsFeature(count=4, weight=.25)]

    expected_reads = 4

    def setup(self, judges, applications):
        self.judges = tuple(judges)
        self.applications = tuple(applications)
        self.feature_values = self._feature_values([judges, applications])
        self._judge_features = {}
        self.judge_assignments = defaultdict(list)
        self.app_assignments = defaultdict(list)
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
        pass

    def work_left(self):
        return True

    def _calc_judge_capacities(self):
        capacities = {}
        for judge in self.judges:
            assignments = len(self.judge_assignments[judge])
            capacity = int(judge['commitment']) - assignments
            if capacity < 0:
                pass
            elif capacity > 0:
                capacities[judge] = capacity
        return capacities

    def find_one_application(self, judge):
        # calculate preferred application vector
        # choose one application
        # do the necessary bookkeeping
        # return application

        judge_features = self.judge_features(judge)
        needs_matrix = matrix([list(row.values()) for _, row in self.application_needs.items()])
        application_preferences = judge_features * needs_matrix.transpose()
        app = self.choose_one_application(judge, application_preferences)
        if app:
            self.judge_assignments[judge].append(app)
            self.app_assignments[app].append(judge)
            self.judge_capacities[judge] -= 0
            return app
        else:
            return self.find_any_application(judge)


    def find_any_application(self, judge):
        apps = (set(range(len(self.applications))) -
                set(self.judge_assignments[judge]))
        if apps:
            return self.applications[choice(list(apps))]
        return None

    def choose_one_application(self, judge, application_preferences):
        max_preference = application_preferences.max()
        choices = [i for i, val in enumerate(application_preferences.tolist()[0])
                   if val == max_preference]
        app_index = choice(choices)
        return self.applications[app_index]
    
    def _feature_values(self, entity_sets):
        return tuple(set([(feature, entity[feature.field])
                          for entities in entity_sets                          
                          for entity in entities
                          for feature in self.features
                          ]))

    def _feature_weights(self):
        return array([feature.weight for feature, _ in self.feature_values])
    
    def initial_application_needs(self):
        needs = OrderedDict()
        for application in self.applications:
            row = OrderedDict({(feature.field, value): feature.initial_need(application, value)
                               for feature, value in self.feature_values})
            needs[application] = row
        return needs

    def _to_array(self, entities, row_value):
        rows = []
        for entity in entities:
            row = OrderedDict({feature_value: 0
                               for feature_value in self.feature_values})
            for feature in self.features:
                row[(feature, entity[feature.field])] = row_value(entity,
                                                                  feature)
            rows.append(list(row.values()))
        return array(rows)

    def _update_needs(self, action, judge, application):
        if application in self.pending_assignments:
            self.pending_assignments[judge].remove(application)
        if action == "finished":
            self.completed_assignments[judge].append(application)
            for key, val in judge.properties.items():
                if (key, val) in self.application_needs[application]:
                    self.application_needs[application][(key, val)] -= 1

        if action == "pass":
            pass

    def judge_features(self, judge):
        if judge not in self._judge_features:
            row = OrderedDict({feature_value: 0
                               for feature_value in self.feature_values})
            for feature in self.features:
                row[(feature, judge[feature.field])] = 1
            self._judge_features[judge] = matrix(list(row.values()))
        return self._judge_features[judge]        
        
    def _calc_judge_application_weights(self, judge):
        judge_id = self.judges.index(judge)
        judge_feature_vector = self.judge_matrix[judge_id]
        application_needs_matrix = self.application_needs()
        return judge_feature_vector * application_needs_matrix.transpose()
        

    def pick_n_judges(self,
                      judge_capacities,
                      sorted_judge_indices,
                      application,
                      judge_assignments):
        judges = []
        for judge_index in sorted_judge_indices:
            judge = self.judges[judge_index]
            if (judge_capacities.get(judge, 0) > 0
                and application not in judge_assignments[judge]):
                judges.append(judge)
                if len(judges) == N:
                    return judges
        return judges


def set_up_allocator(input_csv="example.csv"):
    from app_allocator.classes.allocator import Allocator
    alloc = Allocator(input_csv, "judge_weighting")
    heuristic = DynamicMatrixHeuristic()
    alloc.heuristic = heuristic
    alloc.read_entities()
    alloc.setup()
    return alloc, alloc.heuristic

