from app_allocator.classes.application import Application
from app_allocator.classes.judge import Judge


class Generator(object):
    def __init__(self, judge_count=0, application_count=0):
        self.judges = [Judge() for i in range(judge_count)]
        self.applications = [Application() for i in range(application_count)]
