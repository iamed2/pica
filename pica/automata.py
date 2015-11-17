"""
A cellular automata
"""
from collections import namedtuple, Counter
from random import random, choice

from pica.cells import Cells


Change = namedtuple('Change', ('x', 'y', 'state'))


class Automata:
    """
    A cellular automata.
    """
    def __init__(self, width, height, initial_state, *rules):
        self._cells = Cells(width, height, initial_state)
        self._rules = rules

    @property
    def cells(self):
        return self._cells

    def randomize(self, states):
        """
        randomize the automata.

        states: an iterable of possible states.
        """
        if not states:
            raise ValueError(states)

        for x in range(self._cells.width):
            for y in range(self._cells.height):
                self._cells.update(x, y, choice(states))

    def step(self):
        """
        Take a step in the simulation. Returns a set of Changes.
        """
        changes = set()

        for x in range(self._cells.width):
            for y in range(self._cells.height):
                possibilities = Counter()
                forbidden = set()

                for rule in self._rules:
                    rule.reset()

                    result = rule(self._cells, x, y)

                    if result:
                        if result.difference is None:
                            forbidden.add(result.state)
                        else:
                            possibilities[result.state] += result.difference

                for state in forbidden:
                    del possibilities[state]  # works even if state not a key

                total = sum(possibilities.values())

                if total:  # at least one possibility
                    value = total * random()

                    tally = 0
                    for state, probability in possibilities.items():
                        tally += probability

                        if value < tally:
                            if self._cells.cell(x, y) != state:  # new state
                                changes.add(Change(x, y, state))

                            break

        for change in changes:
            self._cells.update(change.x, change.y, change.state)

        return changes
