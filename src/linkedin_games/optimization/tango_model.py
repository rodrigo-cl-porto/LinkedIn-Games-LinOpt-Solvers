import pyomo.environ as pyo

from ..domain.games.tango.tango import Tango

from ._optimization_model import OptimizationModelBuilder


class TangoModelBuilder(OptimizationModelBuilder[Tango]):
    """The Linear Optimization Model for Tango game."""

    def set_range_sets(self) -> None:
        super().set_range_sets()


    def set_composite_sets(self) -> None:
        super().set_composite_sets()
        self._model.K = pyo.Set(initialize=self._game.filled_squares.keys(), dimen=2)
        self._model.M = pyo.Set(initialize=self._game.matching_pairs)
        self._model.O = pyo.Set(initialize=self._game.opposite_pairs)


    def set_decision_variables(self) -> None:
        self._model.x = pyo.Var(self._model.S, domain=pyo.Binary, initialize=0)


    def set_parameters(self) -> None:
        self._model.k = pyo.Param( # Filled values
            self._model.K,
            initialize=self._game.filled_squares, domain=pyo.Binary
        )


    def set_objective_function(self) -> None:
        self._model.obj = pyo.Objective(expr=0) # feasibility problem


    def set_constraints(self) -> None:
        self._model.equal_moons_suns_per_row_constraints = pyo.Constraint(
            self._model.I,
            rule=lambda model, i: pyo.quicksum(model.x[i,j] for j in model.J) == model.n / 2
        )
        self._model.equal_moons_suns_per_column_constraints = pyo.Constraint(
            self._model.J,
            rule=lambda model, j: pyo.quicksum(model.x[i,j] for i in model.I) == model.m / 2
        )
        self._model.no_three_consecutive_moons_per_row_constraints = pyo.Constraint(
            self._model.I, pyo.RangeSet(self._model.n - 2),
            rule=lambda model, i, j: model.x[i,j] + model.x[i, j+1] + model.x[i, j+2] <= 2
        )
        self._model.no_three_consecutive_suns_per_row_constraints = pyo.Constraint(
            self._model.I, pyo.RangeSet(self._model.n-2),
            rule=lambda model, i, j: model.x[i,j] + model.x[i, j+1] + model.x[i, j+2] >= 1
        )
        self._model.no_three_consecutive_moons_per_column_constraints = pyo.Constraint(
            pyo.RangeSet(self._model.m - 2), self._model.J,
            rule=lambda model, i, j: model.x[i,j] + model.x[i+1, j] + model.x[i+2, j] <= 2
        )
        self._model.no_three_consecutive_suns_per_column_constraints = pyo.Constraint(
            pyo.RangeSet(self._model.m - 2), self._model.J,
            rule=lambda model, i, j: model.x[i,j] + model.x[i+1, j] + model.x[i+2, j] >= 1
        )
        self._model.already_filled_squares_constraints = pyo.Constraint(
            self._model.K,
            rule=lambda model, i, j: model.x[i,j] == model.k[i,j]
        )
        self._model.matching_pairs_constraints = pyo.Constraint(
            self._model.M,
            rule=lambda model, i, j, r, s: model.x[i,j] - model.x[r, s] == 0
        )
        self._model.opposite_pairs_constraints = pyo.Constraint(
            self._model.O,
            rule=lambda model, i, j, r, s: model.x[i,j] + model.x[r, s] == 1
        )
