class Heuristic(object):
    registered_heuristics = []

    def process_judge_events(self, events):
        for event in events:
            action = event.fields.get("action")
            judge = event.fields.get("subject")
            application = event.fields.get("object")
            if action and judge and application:
                self._update_needs(action, judge, application)

    @classmethod
    def register_heuristic(klass, heuristic):
        klass.registered_heuristics.append(heuristic)


def find_heuristic(name):
    for heuristic in Heuristic.registered_heuristics:
        if heuristic.name == name:
            return heuristic()
    return Heuristic.registered_heuristics[0]()
