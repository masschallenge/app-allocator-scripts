from random import choice
from collections import defaultdict, OrderedDict
from numpy import matrix, array
from app_allocator.classes.judge_feature import JudgeFeature
from app_allocator.classes.reads_feature import ReadsFeature
from app_allocator.classes.matching_feature import MatchingFeature
from app_allocator.classes.option_spec import OptionSpec

REFRESH_TIME = 100
N = 2

class JudgeWeightingHeuristic(object):
    ticks = 0
    name = "judge_weighting"
    features = [MatchingFeature("industry"),
                MatchingFeature("program"),
                JudgeFeature("role",
                             option_specs=[OptionSpec("Executive", 2),
                                           OptionSpec("Investor"),
                                           OptionSpec("Lawyer")]),
                JudgeFeature("gender", weight=.9, option_specs=[OptionSpec("female"),
                                                                OptionSpec("male")]),
                ReadsFeature(count=4)]                
    
    expected_reads = 4
    
    def setup(self, judges, startups):
        self.completed_assignments = defaultdict(list)
        self.pending_assignments = defaultdict(list)        
        self.judges = tuple(judges)
        self.startups = tuple(startups)
        self.judge_assignments = defaultdict(list)
        self.feature_value_set = self._feature_values(judges)
        self.feature_value_set.update(self._feature_values(startups))
        self.feature_values = list(self.feature_value_set)
        self.feature_weights = [(feature.field, feature.weight) for feature in self.features]
        self.judge_matrix = matrix(self._to_array(judges, judge_row_value))
        self.startup_needs = self._startup_needs()
        self.judge_startup_weights = self._calc_weightings(self.startup_needs)
        judge_assignments = defaultdict(list)
        judge_capacities = self._calc_judge_capacities(judge_assignments)
        self.pre_assignments = self._calc_preassignments(judge_capacities,
                                                         judge_assignments,
                                                         self.startup_needs.copy(),
                                                         N)
        
    def work_left(self):
        return True

    def _calc_judge_capacities(self, judge_assignments):
        capacities = {}
        for judge in self.judges:
            assignments = judge_assignments[judge]
            capacities[judge] = int(judge['commitment']) - len(assignments)
        return capacities
            
        
    def find_one_application(self, judge):
        # row_number = self.judges.index(judge)
        # row = self.judge_startup_weights[row_number]
        # top_app_indexes = self.find_top_app_indexes(row, judge)
        # app_index = choice(top_app_indexes)
        # self.judge_startup_weights[row_number, app_index] = -1
        # app = self.startups[app_index]
        # self.judge_assignments[judge].append(app)
        # if self.ticks % REFRESH_TIME == 0:
        #     self.judge_startup_weights = self._calc_weightings()
        # self.ticks += 1            
        # return self.startups[app_index]
        if self.pre_assignments[judge]:            
            app = self.pre_assignments[judge].pop(0)
            self.pending_assignments[judge].append(app)
            return app
        else:
            return self.find_any_application(judge)

    def find_any_application(self, judge):
        apps = set(range(len(self.startups))) - set(self.completed_judge_assignments[judge])
        if apps:
            return self.startups[choice(apps)]
        return None
    
    def find_top_app_indexes(self, row, judge):
        top_score = max(row)
        return [ix for ix, val in enumerate(row) if val == top_score]

    def process_judge_events(self, events):
        for event in events:
            action = event.fields.get("action")            
            judge = event.fields.get("subject")
            application = event.fields.get("object")
            if action and judge and application:
                self._update_needs(action, judge, application)

    
    def assess(self):
        pass

    def _feature_values(self, entities):
        return set([(feature, entity[feature.field])
                    for entity in entities for feature in self.features])

    def _calc_weightings(self, startup_needs):
        startup_needs_matrix = matrix([list(row.values()) for row in startup_needs.values()])
        return array(self.judge_matrix * (startup_needs_matrix.transpose()))

    def _startup_needs(self):
        needs = OrderedDict()
        for startup in self.startups:
            row = OrderedDict({(feature.field, value): feature.initial_need(startup, value)
                               for feature, value in self.feature_values})
            needs[startup] = row
        return needs


    def _to_array(self, entities, row_value):
        rows = []
        for entity in entities:
            row = OrderedDict({feature_value:0 for feature_value in self.feature_values})
            for feature in self.features:
                row[(feature, entity[feature.field])] = row_value(entity, feature)
            rows.append(list(row.values()))
        return array(rows)

    def _update_needs(self, action, judge, startup):
        self.pending_assignments[judge].remove(startup)
        if action == "finished":
            self.completed_assignments[judge].append(startup)
            for key, val in judge.properties.items():
                if (key, val) in self.startup_needs[startup]:
                    self.startup_needs[startup][(key, val)] -= 1

        if action == "pass":
            pass
            

    def _calc_preassignments(self,
                             judge_capacities,
                             judge_assignments,
                             startup_needs,
                             n):
        '''
        Starting with applications with the greatest potential weight across all judges,
        find the judges with remaining capacity that can provide the greatest value.
        Randomly select one or more of these judges and pre-assign this application to
        those judges. The number to select should be a parameter that we can experiment
        with.
        
        Once each application has been pre-assigned once in a given pass, recalculate
        the weights for each judge/application pair taking into account any previous
        pre-assignments, and repeat the pre-assignment process while ensuring that a
        given application does not get pre-assigned to the same judge. Repeat this
        process until all current judge capacity has been pre-assigned.
        '''
        while any(judge_capacities.values()):
            judge_startup_weights = self._calc_weightings(startup_needs)            
            maxes = judge_startup_weights.max(0)
            sorted_by_max_weights = [ix for ix, _ in sorted(enumerate(maxes),
                                                            key = lambda t: t[1],
                                                            reverse = True)]
                                     
            count = 0
            for index in sorted_by_max_weights:
                self.pre_assign(index, n,  judge_capacities, judge_assignments, startup_needs)
            
        return judge_assignments

    def pre_assign(self, startup_index, n, judge_capacities, judge_assignments, startup_needs):
        startup = self.startups[startup_index]
        startup_row = self.judge_startup_weights.transpose()[startup_index]
        sorted_judge_indices = [index for index, _ in sorted(enumerate(startup_row),
                                                             key=lambda t: t[1],
                                                             reverse=True)]
        judges = self.pick_n_judges(judge_capacities, sorted_judge_indices, startup, n, judge_assignments)
        startup = self.startups[startup_index]
        for judge in judges:
            judge_assignments[judge].append(startup)
            judge_capacities[judge] -= 1
            for key, val in judge.properties.items():
                if (key, val) in startup_needs[startup]:
                    startup_needs[startup][(key, val)] -= 1

    def pick_n_judges(self, judge_capacities, sorted_judge_indices, startup, n, judge_assignments):
        judges = []
        for judge_index in sorted_judge_indices:
            judge = self.judges[judge_index]
            if judge_capacities.get(judge) and startup not in judge_assignments[judge]:
                judges.append(judge)
                if len(judges) == n:
                    return judges
        return judges

    
def judge_row_value(judge, feature):
    return feature.weight

def startup_row_value(startup, feature):
    return startup_needs[startup][feature]

def set_up_allocator():
    from app_allocator.classes.allocator import Allocator
    alloc = Allocator("example.csv", "judge_weighting")
    heuristic = JudgeWeightingHeuristic()
    alloc.heuristic = heuristic
    alloc.read_entities()
    alloc.setup()
    return alloc, alloc.heuristic
