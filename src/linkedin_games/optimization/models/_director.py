from pyomo.environ import ConcreteModel

from ...domain.games.game_grid import GameGrid
from ._factory import OptimizationModelBuilderFactory


class OptimizationModelDirector:
    @staticmethod
    def build_opt_model(game: GameGrid) -> ConcreteModel:
        builder = OptimizationModelBuilderFactory.create(game)
        return (
            builder
            .set_board_dimensions()
            .set_range_sets()
            .set_composite_sets()
            .set_parameters()
            .set_decision_variables()
            .set_objective_function()
            .set_constraints()
            .build()
        )
