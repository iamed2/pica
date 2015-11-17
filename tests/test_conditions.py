"""
Tests for the cells module.
"""
from nose.tools import assert_equals, assert_raises, assert_true, assert_false


def test_condition():
    """
    The Condition object
    """
    from pica.conditions import Condition

    with assert_raises(TypeError):
        Condition()

    class Implementation(Condition):
        """
        An implementation of the Condition class
        """
        def __init__(self):
            super().__init__()

            self._counter = 0

        def evaluate(self, cells, x, y):
            """
            An implementation of evaluate.
            """
            self._counter += 1

            return self._counter - 1

    condition = Implementation()

    assert_equals(condition(None, None, None), 0)
    assert_equals(condition(None, None, None), 0)
    assert_equals(condition(None, None, None), 0)
    assert_equals(condition(None, None, None), 0)

    condition.reset()

    assert_equals(condition(None, None, None), 1)
    assert_equals(condition(None, None, None), 1)

    condition.reset()
    condition.reset()

    assert_equals(condition(None, None, None), 2)


def test_equals():
    """
    Equals condition
    """
    from pica.cells import Cells
    from pica.conditions import Equals

    cells = Cells(2, 2, 'different')
    cells.update(0, 0, 'same')
    cells.update(1, 1, 'same')

    # no matching states
    no_matching = Equals(0, 0)
    match_same = Equals(0, 0, 'same')
    match_all = Equals(0, 0, 'same', 'different')
    match_offset = Equals(1, 0, 'same')

    assert_false(no_matching(cells, -1, -1))
    assert_false(match_same(cells, -1, -1))
    assert_false(match_all(cells, -1, -1))
    assert_false(match_offset(cells, -1, -1))

    for x in range(2):
        for y in range(2):
            no_matching.reset()
            assert_false(no_matching(cells, x, y))

            match_same.reset()
            assert_equals(match_same(cells, x, y), x == y)

            match_all.reset()
            assert_true(match_all(cells, x, y))

            match_offset.reset()
            assert_equals(match_offset(cells, x, y), x + 1 == y)


def test_compound_condition():
    """
    The CompoundCondition object
    """
    from pica.cells import Cells
    from pica.conditions import Condition, CompoundCondition, Equals

    cells = Cells(2, 2, 'different')
    cells.update(0, 0, 'same')
    cells.update(1, 1, 'same')

    with assert_raises(TypeError):
        CompoundCondition()

    class TestCondition(Condition):
        """
        An implementation of the Condition class
        """
        def __init__(self):
            super().__init__()

            self._counter = 0

        def evaluate(self, cells, x, y):
            """
            An implementation of evaluate.
            """
            self._counter += 1

            return self._counter - 1

    class Implementation(CompoundCondition):
        """
        An implementation of the Condition class
        """
        def __init__(self, condition):
            super().__init__()

            self._condition = condition

        @property
        def conditions(self):
            return (self._condition,)

        def evaluate(self, cells, x, y):
            """
            An implementation of evaluate.
            """
            return self._condition(cells, x, y)

    condition = Implementation(Equals(0, 0, 'same'))

    assert_true(condition(cells, 0, 0))
    condition.reset()

    assert_false(condition(cells, 0, 1))
    condition.reset()

    condition = Implementation(TestCondition())

    assert_equals(condition(cells, 0, 0), 0)
    assert_equals(condition(cells, 0, 0), 0)
    assert_equals(condition(cells, 0, 0), 0)
    assert_equals(condition(cells, 0, 0), 0)
    condition.reset()

    assert_equals(condition(cells, 0, 0), 1)
    assert_equals(condition(cells, 0, 0), 1)
    assert_equals(condition(cells, 0, 0), 1)
    assert_equals(condition(cells, 0, 0), 1)
    condition.reset()


def test_not():
    """
    Not condition
    """
    from pica.cells import Cells
    from pica.conditions import Equals, Not

    cells = Cells(2, 2, 'different')
    cells.update(0, 0, 'same')
    cells.update(1, 1, 'same')

    # no matching states
    not_no_matching = Not(Equals(0, 0))
    not_match_same = Not(Equals(0, 0, 'same'))
    not_match_all = Not(Equals(0, 0, 'same', 'different'))
    not_match_offset = Not(Equals(1, 0, 'same'))
    not_not_match_same = Not(Not(Equals(0, 0, 'same')))

    assert_true(not_no_matching(cells, -1, -1))
    assert_true(not_match_same(cells, -1, -1))
    assert_true(not_match_all(cells, -1, -1))
    assert_true(not_match_offset(cells, -1, -1))

    for x in range(2):
        for y in range(2):
            not_no_matching.reset()
            assert_true(not_no_matching(cells, x, y))

            not_match_same.reset()
            assert_equals(not_match_same(cells, x, y), x != y)

            not_match_all.reset()
            assert_false(not_match_all(cells, x, y))

            not_match_offset.reset()
            assert_equals(not_match_offset(cells, x, y), x + 1 != y)

            not_not_match_same.reset()
            assert_equals(not_not_match_same(cells, x, y), x == y)


def test_and():
    """
    And condition
    """
    from pica.cells import Cells
    from pica.conditions import Equals, And

    cells = Cells(2, 2, 'different')
    cells.update(0, 0, 'same')
    cells.update(1, 1, 'same')

    match_same = And(Equals(0, 0, 'same'), Equals(0, 0, 'same', 'different'))
    match_never = And(Equals(0, 0, 'same'), Equals(0, 0))

    assert_false(match_same(cells, -1, -1))
    assert_false(match_never(cells, -1, -1))

    for x in range(2):
        for y in range(2):
            match_same.reset()
            assert_equals(match_same(cells, x, y), x == y)

            match_never.reset()
            assert_false(match_never(cells, x, y))


def test_or():
    """
    Or condition
    """
    from pica.cells import Cells
    from pica.conditions import Equals, Or

    cells = Cells(2, 2, 'different')
    cells.update(0, 0, 'same')
    cells.update(1, 1, 'same')

    match_always = Or(Equals(0, 0, 'same'), Equals(0, 0, 'same', 'different'))
    match_same = Or(Equals(0, 0, 'same'), Equals(0, 0))

    assert_false(match_always(cells, -1, -1))
    assert_false(match_same(cells, -1, -1))

    for x in range(2):
        for y in range(2):
            match_always.reset()
            assert_true(match_always(cells, x, y))

            match_same.reset()
            assert_equals(match_same(cells, x, y), x == y)


def test_in_range():
    """
    InRange condition
    """
    from pica.cells import Cells
    from pica.conditions import Equals, InRange

    cells = Cells(2, 2, 'different')
    cells.update(0, 0, 'same')
    cells.update(1, 1, 'same')

    conditions = (
        Equals(0, 0), Equals(0, 0, 'same'), Equals(0, 0, 'same', 'different')
    )

    two = InRange(*conditions, lower=2, upper=2)
    fewer_than_two = InRange(*conditions, upper=1)
    at_least_one = InRange(*conditions, lower=1)

    assert_false(two(cells, -1, -1))
    assert_true(fewer_than_two(cells, -1, -1))
    assert_false(at_least_one(cells, -1, -1))

    for x in range(2):
        for y in range(2):
            two.reset()
            assert_equals(two(cells, x, y), x == y)

            fewer_than_two.reset()
            assert_equals(fewer_than_two(cells, x, y), x != y)

            at_least_one.reset()
            assert_true(at_least_one(cells, x, y))


def test_if():
    """
    If condition
    """
    from pica.cells import Cells
    from pica.conditions import Equals, If, Not

    cells = Cells(2, 2, 'different')
    cells.update(0, 0, 'same')
    cells.update(1, 1, 'ones')

    # This could be expressed easier, but that's fine
    ones = If(Not(Equals(0, 0, 'different')), Equals(0, 0, 'ones'))
    same_or_ones = If(
        Equals(0, 0, 'ones'), Equals(0, 0, 'ones'), Equals(0, 0, 'same')
    )

    assert_false(ones(cells, -1, -1))
    assert_false(same_or_ones(cells, -1, -1))

    for x in range(2):
        for y in range(2):
            ones.reset()
            assert_equals(ones(cells, x, y), x == y == 1)

            same_or_ones.reset()
            assert_equals(same_or_ones(cells, x, y), x == y)
