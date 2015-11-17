"""
Tests for the cells module.
"""
from nose.tools import assert_equals, assert_is_none, assert_raises


def test_cells():
    """
    Create a Cells object
    """
    from pica.cells import Cells

    cells = Cells(3, 2, 'state')

    assert_equals(cells.width, 3)
    assert_equals(cells.height, 2)

    for x in range(3):
        for y in range(2):
            assert_equals(cells.cell(x, y), 'state')

    for x, y in ((-1, -1), (0, 4), (3, 2)):
        assert_is_none(cells.cell(x, y))

    for y in (-1, 2, 3):
        with assert_raises(ValueError):
            # because row is a generator, we can't just call cells.row,
            # as the ValueError won't be thrown until access.
            list(cells.row(y))

    for y in range(2):
        for cell in cells.row(y):
            assert_equals(cell, 'state')

    for x, y in ((-1, -1), (0, 4), (3, 2)):
        with assert_raises(ValueError):
            cells.update(x, y, 'new state')

    for y in range(2):
        for cell in cells.row(y):
            assert_equals(cell, 'state')

    for x in range(3):
        for y in range(2):
            assert_equals(cells.cell(x, y), 'state')

            cells.update(x, y, (x, y))

            assert_equals(cells.cell(x, y), (x, y))

    for y in range(2):
        for x, cell in enumerate(cells.row(y)):
            assert_equals(cell, (x, y))
