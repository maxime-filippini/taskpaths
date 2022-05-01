from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Callable


class BaseStep(ABC):
    """
    Base class for Step subclasses
    """

    has_run = False

    @abstractmethod
    def run(self):
        pass

    @property
    def id_(self):
        return self._id

    @id_.setter
    def id_(self, v):
        self._id = v

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v

    @property
    def precedents(self):
        return self._precedents

    @precedents.setter
    def precedents(self, v):
        self._precedents = v

    def pipe(self, other: Step):
        other.precedents.append(self)
        return other

    def __rshift__(self, other: Step):
        return self.pipe(other)


@dataclass
class Step(BaseStep):
    id_: str
    precedents: list[Step] = field(default_factory=list)
    value: Any = field(init=False)

    @abstractmethod
    def instruction(self):
        pass

    def _validate(self):
        """To be implemented"""

    def run(self):
        # Compute values of precedents, using recursion
        for precedent in self.precedents:
            if not precedent.has_run:
                precedent.run()

        # Store the outputs
        prec_dict = {p.id_: p.value for p in self.precedents}
        self.value = self.instruction(**prec_dict)


@dataclass
class LambdaStep(Step):
    lambda_: Callable = lambda x: x

    def instruction(self, *args, **kwargs):
        return self.lambda_(*args, **kwargs)


class InputStep(Step):
    has_run = True
    max_precedent = 0

    def __init__(self, id_: str, value: Any):
        self._id = id_
        self._value = value

    def instruction(self):
        return self._value
