from app_allocator.classes.entity import Entity
from app_allocator.classes.property import (
    industry,
    name,
    program,
)


class Application(Entity):
    def __init__(self, data=None):
        super().__init__()
        self.zscore_sum = 0
        self.zscore_count = 0
        self.judges = []
        self.type = "application"
        self.add_property(name, data)
        self.add_property(industry, data)
        self.add_property(program, data)

    def assign_judge(self, judge):
        self.zscore_sum += (1 - judge.chance_of_pass) * judge.zscore()
        self.zscore_count += 1
        self.judges.append(judge)

    def process_judge_action(self, action, judge):
        if action == "finished":
            self.judge_completed(judge)
        elif action == "pass":
            self.judge_skip(judge)

    def judge_completed(self, judge):
        if judge in self.judges:
            self.zscore_sum += judge.chance_of_pass * judge.zscore()

    def judge_skip(self, judge):
        if judge in self.judges:
            self.zscore_sum -= (1 - judge.chance_of_pass) * judge.zscore()
            self.zscore_count -= 1

    def estimated_zscore(self):
        return self.zscore_sum / self.zscore_count

    def expected_zscore(self, new_value):
        return (self.zscore_sum + new_value) / (self.zscore_count + 1)
