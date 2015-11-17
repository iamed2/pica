"""
The cells within a cellular automata
"""


class Cells:
    """
    A collection of cells in a cellular automata
    """
    def __init__(self, width, height, initial_state):
        self._width = width
        self._height = height

        self._cells = []

        for _ in range(height):
            self._cells.append([initial_state for _ in range(width)])

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def cell(self, x, y):
        """
        Get the value of the cell (or None if that cell is not in range)

        x: the x position of the cell.
        y: the y position of the cell.
        """
        if 0 <= y < self._height and 0 <= x < self._width:
            return self._cells[y][x]

    def row(self, y):
        """
        A generator for enumerating over a row of the cells.

        y: the y position of the cell.
        """
        if y < 0 or y >= self._height:
            raise ValueError(y)

        for cell in self._cells[y]:
            yield cell

    def update(self, x, y, state):
        """
        Update a cell.

        x: the x position of the cell.
        y: the y position of the cell.
        state: The state to set the cell to.
        """
        if x < 0 or x >= self._width:
            raise ValueError(x)

        if y < 0 or y >= self._height:
            raise ValueError(y)

        self._cells[y][x] = state
