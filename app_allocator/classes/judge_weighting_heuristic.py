from copy import deepcopy
from random import choice
from collections import defaultdict, OrderedDict
from numpy import matrix, array
from app_allocator.classes.judge_feature import JudgeFeature
from app_allocator.classes.reads_feature import ReadsFeature
from app_allocator.classes.matching_feature import MatchingFeature
from app_allocator.classes.option_spec import OptionSpec

REFRESH_TIME = 1000
N = 1

class JudgeWeightingHeuristic(object):
    ticks = 0
    name = "judge_weighting"
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

    def setup(self, judges, startups):
        self.completed_assignments = defaultdict(list)
        self.pending_assignments = defaultdict(list)
        self.judges = tuple(judges)
        for judge in judges:
            judge.properties['reads']=''
        self.startups = tuple(startups)
        self.judge_assignments = defaultdict(list)
        feature_value_set = self._feature_values(judges)
        feature_value_set.update(self._feature_values(startups))
        self.feature_values = list(feature_value_set)
        self.judge_matrix = matrix(self._to_array(judges, judge_row_value))
        self.startup_needs = self._startup_needs()
        self.judge_startup_weights = self._calc_weightings(self.startup_needs)
        judge_assignments = defaultdict(list)
        self.judge_capacities = self._calc_judge_capacities(judge_assignments)
        self.pre_assignments = self._calc_preassignments(
            judge_assignments)

    def work_left(self):
        return self.ticks < 9000000

    def _calc_judge_capacities(self, judge_assignments):
        capacities = {}
        for judge in self.judges:
            assignments = len(judge_assignments[judge])
            capacity = int(judge['commitment']) - assignments
            if capacity < 0:
                pass
            elif capacity > 0:
                capacities[judge] = capacity
        return capacities

    def find_one_application(self, judge):
        self.ticks += 1
        if self.ticks % REFRESH_TIME == 0:
            self.pre_assignments = self._calc_preassignments(
                self.completed_assignments)
        if self.judge_capacities[judge] <= 0:
            return None
        if self.pre_assignments[judge]:
            app = self.pre_assignments[judge].pop(0)
            while app in self.pending_assignments[judge] and self.pre_assignments[judge]:
                app = self.pre_assignments[judge].pop()
            self.pending_assignments[judge].append(app)
            self.judge_capacities[judge] -= 0
            return app
        else:
            return self.find_any_application(judge)

    def find_any_application(self, judge):
        apps = (set(range(len(self.startups))) -
                set(self.completed_assignments[judge]))
        if apps:
            return self.startups[choice(list(apps))]
        return None

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

    def _feature_weights(self):
        return array([feature.weight for feature, _ in self.feature_values])
    
    def _calc_weightings(self, startup_needs):
        startup_needs_array = array([list(row.values())
                                     for row in startup_needs.values()])
        startup_needs_array *= self._feature_weights()
        startup_needs_matrix = matrix(startup_needs_array)
        #return array(self.judge_matrix * (startup_needs_matrix.transpose()))
        result = array(self.judge_matrix * (startup_needs_matrix.transpose()))
        return result

    def _startup_needs(self, existing_assignments=None):
        needs = OrderedDict()
        for startup in self.startups:
            row = OrderedDict({(feature.field, value): feature.initial_need(startup, value)
                               for feature, value in self.feature_values})
            needs[startup] = row
        if existing_assignments:
            for judge, assignments in existing_assignments.items():
                for startup in assignments:
                    for field, value in judge.properties.items():
                        if (field, value) in needs[startup]:
                            needs[startup][(field, value)] -= 1
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

    def _update_needs(self, action, judge, startup):
        if startup in self.pending_assignments:
            self.pending_assignments[judge].remove(startup)
        if action == "finished":
            self.completed_assignments[judge].append(startup)
            for key, val in judge.properties.items():
                if (key, val) in self.startup_needs[startup]:
                    self.startup_needs[startup][(key, val)] -= 1

        if action == "pass":
            pass

    def _calc_preassignments(self,
                             existing_judge_assignments):
        '''
        Starting with applications with the greatest potential weight across
        all judges, find the judges with remaining capacity that can provide
        the greatest value. Randomly select one or more of these judges and
        pre-assign this application to those judges. The number to select
        should be a parameter that we can experiment with.

        Once each application has been pre-assigned once in a given pass,
        recalculate the weights for each judge/application pair taking into
        account any previous pre-assignments, and repeat the pre-assignment
        process while ensuring that a given application does not get
        pre-assigned to the same judge. Repeat this process until all current
        judge capacity has been pre-assigned.
        '''
        new_judge_assignments = defaultdict(list)
        judge_capacities = self._calc_judge_capacities(existing_judge_assignments)
        startup_needs = self._startup_needs(existing_judge_assignments)
        while any(judge_capacities.values()):
            judge_startup_weights = self._calc_weightings(startup_needs)
            maxes = judge_startup_weights.max(0).flat
            sorted_indexes = [ix for ix, val in sorted(enumerate(maxes),
                                                       key=lambda t: t[1],
                                                       reverse=True)
                              if val > 0]
            if not sorted_indexes:
                return new_judge_assignments
            for index in sorted_indexes:
                self.pre_assign(index,
                                judge_capacities,
                                existing_judge_assignments,
                                new_judge_assignments,
                                startup_needs,
                                judge_startup_weights)
        return new_judge_assignments

    def pre_assign(self, startup_index, judge_capacities,
                   existing_judge_assignments,
                   new_judge_assignments,
                   startup_needs,
                   judge_startup_weights):
        startup = self.startups[startup_index]
        startup_row = judge_startup_weights.transpose()[startup_index]
        sorted_judge_indices = [ix for ix, _ in sorted(enumerate(startup_row),
                                                       key=lambda t: t[1],
                                                       reverse=True)]
        judges = self.pick_n_judges(judge_capacities,
                                    sorted_judge_indices,
                                    startup,
                                    existing_judge_assignments)
        startup = self.startups[startup_index]
        for judge in judges:
            new_judge_assignments[judge].append(startup)
            judge_capacities[judge] -= 1
            if judge_capacities[judge] == 0:
                judge_capacities.pop(judge)
            for key, val in judge.properties.items():
                if (key, val) in startup_needs[startup]:
                    startup_needs[startup][(key, val)] -= 1

    def pick_n_judges(self,
                      judge_capacities,
                      sorted_judge_indices,
                      startup,
                      judge_assignments):
        judges = []
        for judge_index in sorted_judge_indices:
            judge = self.judges[judge_index]
            if (judge_capacities.get(judge, 0) > 0
                and startup not in judge_assignments[judge]):
                judges.append(judge)
                if len(judges) == N:
                    return judges
        return judges


def judge_row_value(judge, feature):
    return float(feature.weight)

def set_up_allocator(input_csv="example.csv"):
    from app_allocator.classes.allocator import Allocator
    alloc = Allocator(input_csv, "judge_weighting")
    heuristic = JudgeWeightingHeuristic()
    alloc.heuristic = heuristic
    alloc.read_entities()
    alloc.setup()
    return alloc, alloc.heuristic

