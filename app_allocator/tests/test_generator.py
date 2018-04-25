from app_allocator.classes.generator import Generator


class TestGenerator(object):
    def test_generator_generates_judges(self):
        generator = Generator(judge_count=10, startup_count=100)
        assert len(generator.judges) == 10

    def test_generator_generates_startups(self):
        generator = Generator(judge_count=10, startup_count=100)
        assert len(generator.startups) == 100
