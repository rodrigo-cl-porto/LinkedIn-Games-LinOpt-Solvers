from abc import ABC, abstractmethod

import pyomo.environ as pyo

from ...domain.game_grid import GameGrid


class OptimizationModelBuilder[G: GameGrid](ABC):

    def __init__(self, game: G) -> None:
        self._game = game
        self._model = pyo.ConcreteModel()


    def _set_board_dimensions(self) -> None:
        m, n = self._game.grid_dims
        self._model.m = pyo.Param(initialize=m, domain=pyo.PositiveIntegers)
        self._model.n = pyo.Param(initialize=n, domain=pyo.PositiveIntegers)


    @abstractmethod
    def _set_range_sets(self) -> None:
        self._model.I = pyo.RangeSet(self._model.m) # Rows
        self._model.J = pyo.RangeSet(self._model.n) # Columns


    @abstractmethod
    def _set_composite_sets(self) -> None:
        self._model.S = pyo.Set(initialize=lambda model: [(i,j) for i in model.I for j in model.J]) # Grid Squares


    @abstractmethod
    def _set_parameters(self) -> None:
        ...


    @abstractmethod
    def _set_decision_variables(self) -> None:
        ...


    @abstractmethod
    def _set_objective_function(self) -> None:
        ...


    @abstractmethod
    def _set_constraints(self) -> None:
        ...


    def build(self) -> pyo.ConcreteModel:
        self._set_board_dimensions()
        self._set_range_sets()
        self._set_composite_sets()
        self._set_parameters()
        self._set_decision_variables()
        self._set_objective_function()
        self._set_constraints()
        return self._model
