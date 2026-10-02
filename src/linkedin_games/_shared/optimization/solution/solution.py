from abc import ABC, abstractmethod
from typing import Any, Self

from pyomo.environ import ConcreteModel


class GameSolution(ABC):

    @property
    def squares(self) -> dict[tuple[int, int], Any]:
        return self._squares

    @abstractmethod
    def build(self, opt_model: ConcreteModel) -> Self:
        self._model = opt_model
        self._set_squares()
        return self

    @abstractmethod
    def _set_squares(self) -> None:
        self._squares: dict[tuple[int, int], Any]
