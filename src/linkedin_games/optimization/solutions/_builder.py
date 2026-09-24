from abc import ABC, abstractmethod

from pyomo.environ import ConcreteModel

from ._solution import GameSolution


class GameSolutionBuilder(ABC):

    def __init__(self) -> None:
        self._solution = GameSolution()


    def build(self, opt_model: ConcreteModel) -> GameSolution:
        self._opt_model = opt_model
        self._set_solution()
        return self._solution


    @abstractmethod
    def _set_solution(self) -> None:
        ...
