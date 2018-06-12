from app_allocator.classes.assignments import (
    closer_by_half,
    second_read,
)


class TestAssignments(object):
    def test_closer_by_half(self):
        assert closer_by_half(2, 1)
        assert closer_by_half(-2, 1)
        assert closer_by_half(2, 0.9)
        assert closer_by_half(-2, 0.9)
        assert not closer_by_half(2, 1.1)
        assert not closer_by_half(-2, 1.1)

    def test_second_read(self):
        current = 0.4
        expected = 0.1
        assert second_read(current, expected)
