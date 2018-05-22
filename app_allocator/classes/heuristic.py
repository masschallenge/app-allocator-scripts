
class Heuristic(object):
    
    def process_judge_events(self, events):
        for event in events:
            action = event.fields.get("action")
            judge = event.fields.get("subject")
            application = event.fields.get("object")
            if action and judge and application:
                self._update_needs(action, judge, application)


    def find_n_applications(self, judge, n):
        batch = []
        for _ in range(n):
            app = self.find_one_application(judge)
            if app:
                batch.append(app)
            else:
                break
        return batch


