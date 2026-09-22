from ._optimization_result import OptimizationResult

from ..domain._game_grid import GameGrid
from abc import ABC, abstractmethod
import pyomo.environ as pyo


class OptimizationModelBuilder[G: GameGrid](ABC):

    def __init__(self, game: G) -> None:
        self._game = game


    def build(self) -> pyo.ConcreteModel:
        self._model = pyo.ConcreteModel()
        self.set_board_dimensions()
        self.set_range_sets()
        self.set_composite_sets()
        self.set_parameters()
        self.set_decision_variables()
        self.set_objective_function()
        self.set_constraints()
        return self._model


    def set_board_dimensions(self) -> None:
        m, n = self._game.grid_dims
        self._model.m = pyo.Param(initialize=m, domain=pyo.PositiveIntegers)
        self._model.n = pyo.Param(initialize=n, domain=pyo.PositiveIntegers)


    @abstractmethod
    def set_range_sets(self) -> None:
        self._model.I = pyo.RangeSet(self._model.m) # Rows
        self._model.J = pyo.RangeSet(self._model.n) # Columns


    @abstractmethod
    def set_composite_sets(self) -> None:
        self._model.S = pyo.Set( # Grid Squares
            initialize=lambda model: [(i,j) for i in model.I for j in model.J]
        )


    @abstractmethod
    def set_parameters(self) -> None:
        ...


    @abstractmethod
    def set_decision_variables(self) -> None:
        ...


    @abstractmethod
    def set_objective_function(self) -> None:
        ...


    @abstractmethod
    def set_constraints(self) -> None:
        ...


    def solve(self) -> OptimizationResult:
        ...
