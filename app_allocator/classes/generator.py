from app_allocator.classes.startup import Startup
from app_allocator.classes.judge import Judge


class Generator(object):
    def __init__(self, judge_count=0, startup_count=0):
        self.judges = [Judge() for i in range(judge_count)]
        self.startups = [Startup() for i in range(startup_count)]
