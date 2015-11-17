"""
Conditions for evaluating cellular automata.
"""
from abc import ABCMeta, abstractmethod, abstractproperty


class Condition(metaclass=ABCMeta):
    """
    A condition to be matched. Once run, it will return the same result
    with no further evaluation being done until the condition is reset.
    """
    def __init__(self):
        self._cached = None

    @abstractmethod
    def evaluate(self, cells, x, y):
        """
        Actually make the evaluation
        """

    def __call__(self, cells, x, y):
        """
        Evaluate the condition using the cached value if possible
        """
        if self._cached is None:
            self._cached = self.evaluate(cells, x, y)

        return self._cached

    def reset(self):
        """
        Reset the condition.
        """
        self._cached = None


class CompoundCondition(Condition):
    """
    A condition that operates on other conditions.
    """
    @abstractproperty
    def conditions(self):
        """
        An iterable of conditions
        """

    def reset(self):
        """
        Reset the condition
        """
        super().reset()

        for condition in self.conditions:
            condition.reset()


class Equals(Condition):
    """
    A condition that evaluates as True if the cell is in an iterable of
    states.
    """
    def __init__(self, x, y, *states):
        super().__init__()

        self._x = x
        self._y = y
        self._states = states

    def evaluate(self, cells, x, y):
        """
        Evaluate the condition.
        """
        return cells.cell(x + self._x, y + self._y) in self._states


class Not(CompoundCondition):
    """
    Inverts a condition
    """
    def __init__(self, condition):
        super().__init__()

        self._condition = condition

    @property
    def conditions(self):
        return (self._condition,)

    def evaluate(self, cells, x, y):
        """
        Evaluate the condition.
        """
        return not self._condition(cells, x, y)


class And(CompoundCondition):
    """
    Returns True if all subconditions match
    """
    def __init__(self, *conditions):
        super().__init__()

        self._conditions = conditions

    @property
    def conditions(self):
        return self._conditions

    def evaluate(self, cells, x, y):
        """
        Evaluate the condition.
        """
        return all(condition(cells, x, y) for condition in self._conditions)


class Or(CompoundCondition):
    """
    Returns True if any subconditions match
    """
    def __init__(self, *conditions):
        super().__init__()

        self._conditions = conditions

    @property
    def conditions(self):
        return self._conditions

    def evaluate(self, cells, x, y):
        """
        Evaluate the condition.
        """
        return any(condition(cells, x, y) for condition in self._conditions)


class InRange(CompoundCondition):
    """
    Returns true if lower <= #matching <= upper.
    """
    def __init__(self, *conditions, lower=0, upper=None):
        super().__init__()

        if upper is None:
            upper = len(conditions)

        self._lower = lower
        self._upper = upper
        self._conditions = conditions

    @property
    def conditions(self):
        return self._conditions

    def evaluate(self, cells, x, y):
        """
        Evaluate the condition.
        """
        count = 0

        for condition in self._conditions:
            if condition(cells, x, y):
                count += 1

            if count > self._upper:
                return False

        if count < self._lower:
            return False

        return True


class If(CompoundCondition):
    """
    If condition then condition else condition
    """
    def __init__(self, if_condition, true_condition, false_condition=None):
        super().__init__()

        self._if_condition = if_condition
        self._true_condition = true_condition
        self._false_condition = false_condition

        if false_condition:
            self._conditions = (if_condition, true_condition, false_condition)
        else:
            self._conditions = (if_condition, true_condition)

    @property
    def conditions(self):
        return self._conditions

    def evaluate(self, cells, x, y):
        """
        Evaluate the condition.
        """
        if self._if_condition(cells, x, y):
            return self._true_condition(cells, x, y)
        elif self._false_condition:
            return self._false_condition(cells, x, y)
        else:
            return False
