"""
Tests for the automata module.
"""
from nose.tools import assert_equals


def test_automata():
    """
    The AbstractRule object
    """
    from pica.conditions import Equals, Not, InRange
    from pica.rules import Rule, Requirement
    from pica.automata import Automata, Change

    neighbors = [
        Equals(x, y, 'live')
        for x in range(-1, 2) for y in range(-1, 2)
        if x != 0 or y != 0
    ]

    rules = [
        Requirement(
            'live', 'dead', Not(InRange(*neighbors, lower=2, upper=3))
        ),
        Requirement(
            'dead', 'live', InRange(*neighbors, lower=3, upper=3)
        ),
        Rule('live', 'dead', Equals(0, 0, 'live'), 1),
        Rule('dead', 'live', Equals(0, 0, 'dead'), 1),
    ]

    automata = Automata(5, 5, 'dead', *rules)
    automata.cells.update(0, 0, 'live')
    automata.cells.update(0, 1, 'live')
    automata.cells.update(1, 0, 'live')

    assert_equals(automata.step(), {Change(1, 1, 'live')})
    assert_equals(automata.step(), set())
    assert_equals(automata.step(), set())
    assert_equals(automata.step(), set())
    assert_equals(automata.step(), set())

    automata = Automata(5, 5, 'dead', *rules)
    automata.cells.update(0, 0, 'live')
    automata.cells.update(2, 0, 'live')
    automata.cells.update(2, 1, 'live')
    automata.cells.update(2, 2, 'live')

    assert_equals(
        automata.step(),
        {
            Change(0, 0, 'dead'),
            Change(1, 0, 'live'),
            Change(2, 0, 'dead'),
            Change(2, 2, 'dead'),
            Change(3, 1, 'live'),
        }
    )

    assert_equals(
        automata.step(),
        {
            Change(1, 0, 'dead'),
            Change(2, 0, 'live'),
            Change(3, 1, 'dead'),
        }
    )

    assert_equals(
        automata.step(),
        {
            Change(2, 0, 'dead'),
            Change(2, 1, 'dead'),
        }
    )

    assert_equals(automata.step(), set())
    assert_equals(automata.step(), set())
