"""
Tests for the rules module.
"""
from nose.tools import assert_equals, assert_raises, assert_is_none


def test_abstract_rule():
    """
    The AbstractRule object
    """
    from pica.cells import Cells
    from pica.conditions import Equals
    from pica.rules import AbstractRule, Result

    with assert_raises(TypeError):
        AbstractRule()

    class Implementation(AbstractRule):
        """
        An implementation of the Condition class
        """
        def __init__(self, from_state, to_state, condition):
            super().__init__()

            self._counter = 0

            self._from_state = from_state
            self._to_state = to_state
            self._condition = condition

        @property
        def from_state(self):
            return self._from_state

        @property
        def condition(self):
            return self._condition

        def evaluate(self, cells, x, y):
            """
            An implementation of evaluate.
            """
            if self._condition(cells, x, y):
                self._counter += 1

                return Result(self._to_state, self._counter - 1)

    rule = Implementation('from', 'to', Equals(0, 0, 'from'))

    cells = Cells(2, 2, 'from')
    cells.update(0, 0, 'no match')
    cells.update(1, 1, 'no match')

    assert_equals(rule(cells, 0, 1), Result('to', 0))
    assert_equals(rule(cells, 0, 1), Result('to', 0))
    assert_equals(rule(cells, 0, 1), Result('to', 0))
    assert_equals(rule(cells, 0, 1), Result('to', 0))
    assert_equals(rule(cells, 0, 1), Result('to', 0))
    rule.reset()

    assert_equals(rule(cells, 0, 1), Result('to', 1))
    assert_equals(rule(cells, 0, 1), Result('to', 1))
    assert_equals(rule(cells, 0, 1), Result('to', 1))
    assert_equals(rule(cells, 0, 1), Result('to', 1))
    assert_equals(rule(cells, 0, 1), Result('to', 1))
    rule.reset()

    assert_is_none(rule(cells, 0, 0))
    rule.reset()

    assert_equals(rule(cells, 0, 1), Result('to', 2))


def test_rule():
    """
    A Rule
    """
    from pica.cells import Cells
    from pica.conditions import Equals
    from pica.rules import Rule, Result

    rule = Rule('from', 'to', Equals(1, 0, 'no match'), 0.5)

    cells = Cells(2, 2, 'from')
    cells.update(0, 0, 'no match')
    cells.update(1, 1, 'no match')

    assert_is_none(rule(cells, -1, -1))
    for x in range(2):
        for y in range(2):
            rule.reset()

            if (x, y) == (0, 1):
                assert_equals(rule(cells, x, y), Result('to', 0.5))
            else:
                assert_is_none(rule(cells, x, y))


def test_requirement():
    """
    A Requirement
    """
    from pica.cells import Cells
    from pica.conditions import Equals
    from pica.rules import Requirement, Result

    requirement = Requirement('from', 'to', Equals(1, 0, 'no match'))

    cells = Cells(2, 2, 'from')
    cells.update(0, 0, 'no match')
    cells.update(1, 1, 'no match')

    assert_is_none(requirement(cells, -1, -1))
    for x in range(2):
        for y in range(2):
            requirement.reset()

            if (x, y) == (0, 1) or x == y:
                assert_is_none(requirement(cells, x, y))
            else:
                assert_equals(requirement(cells, x, y), Result('to', None))
