from abc import ABC, abstractmethod
from typing import Self

import pyomo.environ as pyo

from ...domain._game_grid import GameGrid


class OptimizationModelBuilder[G: GameGrid](ABC):

    def __init__(self, game: G) -> None:
        self._game = game
        self._model = pyo.ConcreteModel()


    def set_board_dimensions(self) -> Self:
        m, n = self._game.grid_dims
        self._model.m = pyo.Param(initialize=m, domain=pyo.PositiveIntegers)
        self._model.n = pyo.Param(initialize=n, domain=pyo.PositiveIntegers)
        return self


    @abstractmethod
    def set_range_sets(self) -> Self:
        self._model.I = pyo.RangeSet(self._model.m) # Rows
        self._model.J = pyo.RangeSet(self._model.n) # Columns
        return self


    @abstractmethod
    def set_composite_sets(self) -> Self:
        self._model.S = pyo.Set(initialize=lambda model: [(i,j) for i in model.I for j in model.J]) # Grid Squares
        return self


    @abstractmethod
    def set_parameters(self) -> Self:
        ...


    @abstractmethod
    def set_decision_variables(self) -> Self:
        ...


    @abstractmethod
    def set_objective_function(self) -> Self:
        ...


    @abstractmethod
    def set_constraints(self) -> Self:
        ...


    def build(self) -> pyo.ConcreteModel:
        return self._model
