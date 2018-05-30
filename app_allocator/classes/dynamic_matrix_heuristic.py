from collections import defaultdict, OrderedDict
from numpy import matrix, array
from app_allocator.classes.judge import DEFAULT_CHANCE_OF_PASS
from app_allocator.classes.heuristic import Heuristic
from app_allocator.classes.matching_criterion import MatchingCriterion

CHANCE_OF_PASS = DEFAULT_CHANCE_OF_PASS
ASSIGNED_VALUE = 1 - CHANCE_OF_PASS
FINISHED_VALUE = CHANCE_OF_PASS

ACTION_TO_ADJUSTMENT = {
    "assigned": ASSIGNED_VALUE,
    "finished": FINISHED_VALUE,
    "pass": -ASSIGNED_VALUE,
}


class DynamicMatrixHeuristic(Heuristic):
    name = "dynamic_matrix"

    def __init__(self, criteria):
        super().__init__()
        self.criteria = criteria
        self.find_count = 0

    def setup(self, judges, applications):
        self.judges = tuple(judges)
        for judge in self.judges:
            judge.properties["reads"] = ""
        self.applications = tuple(applications)
        MatchingCriterion.set_up_all(judges, applications)
        self.criteria_weights = self._criteria_weights()
        self.criteria_values = self.criteria_weights.keys()
        self._judge_features = {}
        self.judge_assignments = defaultdict(list)
        self.judge_capacities = self._calc_judge_capacities()
        self.application_needs = self.initial_application_needs()

    def assess(self):
        pass  # pragma: nocover

    def work_left(self):
        return len(self.applications) > 0

    def _calc_judge_capacities(self):
        return {judge: int(judge['commitment'] or 0) for judge in self.judges}

    def evaluate_application(self, app, application_preferences, needs_matrix):
        index = self.applications.index(app)
        print(application_preferences.flat[index])
        print(needs_matrix[index])

    def evaluate_apps(self, apps, application_preferences, needs_matrix):
        for app in apps:
            self.evaluate_application(app, application_preferences,
                                      needs_matrix)

    def find_app_needing_industry(self, exclude):
        for app in self.applications:
            if app not in exclude:
                industry = app.properties["industry"]
                if all([industry != judge.properties["industry"]
                        for judge in app.judges]):
                    return app

    def find_n_applications(self, judge, batch_size):
        if len(self.applications) <= batch_size:
            can_assign = self._can_assign_func(judge)
            apps = [app for app in self.applications if can_assign(app)]
        else:
            available_batch_size = min(batch_size,
                                       self.judge_capacities[judge])
            judge_features = self.judge_features(judge)
            needs_array = array([list(row.values()) for _, row
                                 in self.application_needs.items()])
            criteria_weights_array = array([v for v in
                                           self.criteria_weights.values()])
            needs_matrix = matrix(needs_array * criteria_weights_array)
            application_preferences = judge_features * needs_matrix.transpose()
            apps = self.choose_n_applications(judge,
                                              application_preferences,
                                              available_batch_size)
        # if apps:  # self.find_count > 1600
        #     app = self.find_app_needing_industry(apps)
        #     import pdb; pdb.set_trace()
        #     self.find_count = 0
        self.find_count += 1
        for app in apps:
            self.judge_assignments[judge].append(app)
            self.judge_capacities[judge] -= 1
            self._update_needs("assigned", judge, app)
        return apps

    def choose_n_applications(self, judge, application_preferences, n):
        applications = (array(self.applications)[
                (-application_preferences).argsort()]).flat
        can_assign = self._can_assign_func(judge)
        filtered = [app for app in applications if can_assign(app)]
        return filtered[:n]

    def _can_assign_func(self, judge):
        '''returns a function which takes an application and returns True
        if the application can be assigned to the judge.
        Presumably this is where we'll put the z-score logic as well.
        '''
        def can_assign_to_judge(application):
            return application not in self.judge_assignments[judge]

        return can_assign_to_judge

    def _criteria_weights(self):
        criteria_weights = {}
        for criterion in self.criteria:
            for spec in criterion.option_specs:
                criteria_weights[(criterion, spec.option)] = float(spec.weight)
        return criteria_weights

    def initial_application_needs(self):
        needs = OrderedDict()

        for application in self.applications:
            row = OrderedDict()
            for criterion in self.criteria:
                row.update(criterion.initial_needs(application))
            needs[application] = row
        return needs

    def _update_needs(self, action, judge, application):
        if action == "assigned":
            self.judge_assignments[judge].append(application)
        adjustment = ACTION_TO_ADJUSTMENT[action]
        needs_dict = self.application_needs[application]
        for key, val in judge.properties.items():
            self._update_specific_need(needs_dict, key, val, adjustment)

    def _update_specific_need(self, needs_dict, key, val, adjustment):
        if (key, val) in needs_dict.keys():
            needs_dict[(key, val)] = needs_dict[(key, val)] - adjustment

    def judge_features(self, judge):
        if judge not in self._judge_features:
            self._calc_judge_features(judge)
        return self._judge_features[judge]

    def _calc_judge_features(self, judge):
        row = OrderedDict([(feature_value, 0)
                           for feature_value in self.criteria_values])
        for criterion in self.criteria:
            if (criterion, judge[criterion.name()]) in self.criteria_values:
                row[(criterion, judge[criterion.name()])] = 1
        self._judge_features[judge] = matrix(list(row.values()))
