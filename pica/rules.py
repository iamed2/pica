from abc import ABCMeta, abstractproperty, abstractmethod
from collections import namedtuple

Result = namedtuple('Result', ('state', 'difference'))


class AbstractRule(metaclass=ABCMeta):
    """
    A rule for a cellular automata
    """
    def __init__(self):
        self._is_cached = False
        self._cached = None

    @abstractproperty
    def from_state(self):
        """
        The state the current cell must be in for this rule to be
        applicable.
        """

    @abstractproperty
    def condition(self):
        """
        Returns the condition the rule is predicated on
        """

    @abstractmethod
    def evaluate(self, cells, x, y):
        """
        The evaluation of the rule
        """

    def __call__(self, cells, x, y):
        """
        Evaluate the rule using the cached value if possible
        """
        if not self._is_cached:
            if self.from_state == cells.cell(x, y):
                self._cached = self.evaluate(cells, x, y)
            else:
                self._cached = None

            self._is_cached = True

        return self._cached

    def reset(self):
        """
        Reset the rule.
        """
        self._cached = None
        self._is_cached = False
        self.condition.reset()


class Rule(AbstractRule):
    """
    A rule for changing between two states.
    """
    def __init__(self, from_state, to_state, condition, change):
        super().__init__()

        self._from_state = from_state
        self._to_state = to_state
        self._condition = condition
        self._change = change

    @property
    def from_state(self):
        return self._from_state

    @property
    def condition(self):
        return self._condition

    def evaluate(self, cells, x, y):
        """
        Evaluate the rule
        """
        if self._condition(cells, x, y):
            return Result(self._to_state, self._change)


class Requirement(AbstractRule):
    """
    Require a condition to be true in order for a transition to be
    allowed.
    """
    def __init__(self, from_state, to_state, condition):
        super().__init__()

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
        Evaluate the rule
        """
        if not self._condition(cells, x, y):
            return Result(self._to_state, None)
