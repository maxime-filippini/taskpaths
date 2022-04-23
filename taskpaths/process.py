from abc import ABC
from abc import abstractmethod


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

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self._value = v


class InputStep(BaseStep):
    has_run = True

    def __init__(self, id_, value):
        self._id = id_
        self._value = value

    def run(self, input_dict=None):
        return self._value


class StandardStep(BaseStep):
    def __init__(self, id_: str, precedents: list[BaseStep]):
        self._id = id_
        self._precedents = precedents
        self._value = None

    @property
    def precedents(self):
        return self._precedents

    @abstractmethod
    def instruction(self):
        pass

    def run(self, input_dict=None):
        if input_dict is None:
            input_dict = {}

        # Compute values of precedents, using recursion
        for precedent in self.precedents:
            if not precedent.has_run:
                precedent.run(input_dict)

        # Store the outputs
        prec_dict = {p.id_: p.value for p in self.precedents}
        self.value = self.instruction(**prec_dict, **input_dict)
