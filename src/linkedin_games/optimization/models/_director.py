from abc import ABC, abstractmethod

import pyomo.environ as pyo

from ...domain._game_grid import GameGrid
from ..builders._builder import OptimizationModelBuilder


class OptimizationModelDirector[G: GameGrid](ABC):

    def __init__(self, game: G) -> None:
        self._builder: OptimizationModelBuilder[G]
        self._set_builder(game)


    @abstractmethod
    def _set_builder(self, game: G) -> None:
        ...


    def build(self) -> pyo.ConcreteModel:
        return (
            self._builder
            .set_board_dimensions()
            .set_range_sets()
            .set_composite_sets()
            .set_parameters()
            .set_decision_variables()
            .set_objective_function()
            .set_constraints()
            .build()
        )
