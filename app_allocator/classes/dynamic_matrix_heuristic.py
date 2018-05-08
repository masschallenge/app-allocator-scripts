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
                                weight=1),
                MatchingFeature("program",
                                weight=1),
                JudgeFeature("role",
                             weight=1,
                             option_specs=[OptionSpec("Executive", 2),
                                           OptionSpec("Investor"),
                                           OptionSpec("Lawyer")]),
                JudgeFeature("gender",
                             weight=.2,
                             option_specs=[OptionSpec("female"),
                                           OptionSpec("male")]),
                ReadsFeature(count=4, weight=.2)]

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
        self.app_assignments = defaultdict(list)
        self.judge_capacities = self._calc_judge_capacities()
        self.application_needs = self.initial_application_needs()

    def process_judge_events(self, events):
        for event in events:
            action = event.fields.get("action")
            judge = event.fields.get("subject")
            application = event.fields.get("object")
            # if action and judge and application:
            #     self._update_needs(action, judge, application)

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

    def _calc_needs_matrix(self):
        return matrix([list(row.values()) for _, row in self.application_needs.items()])
    
    def find_one_application(self, judge):
        self.ticks += 1
        judge_features = self.judge_features(judge)
        needs_matrix = self._calc_needs_matrix()
        application_preferences = judge_features * needs_matrix.transpose()
        app = self.choose_one_application(judge, application_preferences)
        if app:
            # if self.ticks > 6000 and self.ticks % 1000== 0:
            #     import pdb; pdb.set_trace()
            # if "dummy" in judge['name']:
            #     import pdb; pdb.set_trace()
            self.judge_assignments[judge].append(app)
            self.app_assignments[app].append(judge)
            self.judge_capacities[judge] -= 1
            self._update_needs("finished", judge, app)
            return app
        else:
            return self.find_any_application(judge)

    def find_any_application(self, judge):
        apps = (set(self.applications) -
                set(self.judge_assignments[judge]))
        if apps:
            return choice(list(apps))
        return None

    def choose_one_application(self, judge, application_preferences):
        applications = (array(self.applications)[application_preferences.argsort()]).flat
        
        can_assign_to_judge = self._can_assign_func(judge)
        applications = filter(can_assign_to_judge, applications)
        return next (applications)


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
#        return array([1 for feature, _ in self.feature_values])

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
        if action == "finished":
            for key, val in judge.properties.items():
                if (key, val) in self.application_needs[application]:
                    self.application_needs[application][(key, val)] = (
                        max(0,
                            self.application_needs[application][(key, val)]
                            - self.feature_weights[(key, val)]))
                    if self.application_needs[application][(key, val)] == 0:
                        self.update_needs_and_features(key, val)
        if action == "pass":
            pass


    def update_needs_and_features(self, key, val):
        if not any([row[(key, val)] for row in self.application_needs.values()]):
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
