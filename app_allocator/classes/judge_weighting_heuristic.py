from collections import defaultdict, OrderedDict
from numpy import matrix, array
from app_allocator.classes.judge_feature import JudgeFeature
from app_allocator.classes.matching_feature import MatchingFeature
from app_allocator.classes.option_spec import OptionSpec

class JudgeWeightingHeuristic(object):
    name = "judge_weighting"
    
    features = [MatchingFeature("industry"),
                MatchingFeature("program"),
                JudgeFeature("role",
                             option_specs=[OptionSpec("Executive", 2),
                                           OptionSpec("Investor"),
                                           OptionSpec("Lawyer")]),
                JudgeFeature("gender", option_specs=[OptionSpec("female"),
                                                     OptionSpec("male")])]
    expected_reads = 4
    
    def setup(self, judges, startups):
        self.judges = tuple(judges)
        self.startups = tuple(startups)
        self.feature_value_set = self._feature_values(judges)
        self.feature_value_set.update(self._feature_values(startups))
        self.feature_values = list(self.feature_value_set)
        self.feature_weights = [(feature.field, 1) for feature in self.features]
        self.judge_matrix = matrix(self._to_array(judges, judge_row_value))
        self.startup_needs = self._startup_needs()
        self.judge_startup_weights = self._calc_weightings()
        
    def work_left(self):
        return True
    
    def find_one_application(self, judge):
        row_number = self.judges.index(judge)
        row = self.judge_startup_weights[row_number]
        top_app_indexes = self.find_top_app_indexes(row, judge)
        return self.startups[choice(top_app_indexes)]

    def find_top_app_indexes(self, row, judge):
        top_score = max(row)
        return [ix for ix, val in enumerate(row) if val == top_score]
    
    def assess(self):
        pass

    def _feature_values(self, entities):
        return set([(feature, entity[feature.field])
                    for entity in entities for feature in self.features])

    def _calc_weightings(self):
        startup_needs_matrix = matrix([list(row.values()) for row in self.startup_needs.values()])

                                      
        return array(self.judge_matrix * (startup_needs_matrix.transpose()))
    
    def _startup_needs(self):
        needs = OrderedDict()
        for startup in self.startups:
            row = OrderedDict({(feature, value): feature.initial_need(startup, value)
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

    def update_startup_needs(self, judge, startup):
        for key, val in judge.properties.items():
            if (key, val) in self.startup_needs[startup]:
                self.startup_needs[(key, val)] -= 1

def calc_judge_startup_weights(startups):
    startups_matrix = matrix(self._to_array(startups))
    weights = judges * startups
    best_judges = weights.argmax(0) # 0? Might be 1

    
def judge_row_value(judge, feature):
    return 1

def startup_row_value(startup, feature):
    return startup_needs[startup][feature]
