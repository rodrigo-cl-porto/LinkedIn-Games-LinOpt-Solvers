from typing import Self

import pyomo.environ as pyo

from ...domain.games.queens.queens import Queens
from ._builder import OptimizationModelBuilder


class QueensModelBuilder(OptimizationModelBuilder[Queens]):

    def set_range_sets(self) -> Self:
        super().set_range_sets()
        self._model.K = pyo.Set(initialize=self._game.regions.keys()) # Colored Regions
        return self


    def set_composite_sets(self) -> Self:
        super().set_composite_sets()
        self._model.R = pyo.Set( # Region Squares
            self._model.K,
            initialize=self._game.regions,
            dimen=2,
            domain=self._model.S
        )
        self._model.D = pyo.Set( # Diagonals
            initialize=lambda model:
                [((i, j), (i + 1, j + 1)) for (i, j) in model.S if (i + 1, j + 1) in model.S] +
                [((i, j), (i + 1, j - 1)) for (i, j) in model.S if (i + 1, j - 1) in model.S]
        )
        return self


    def set_objective_function(self) -> Self:
        self._model.obj = pyo.Objective(expr=0) # feasibility problem
        return self


    def set_decision_variables(self) -> Self:
        self._model.x = pyo.Var(self._model.S, domain=pyo.Binary, initialize=0)
        return self


    def set_constraints(self) -> Self:
        self._model.single_crown_per_row_constraints = pyo.Constraint(
            self._model.I,
            rule=lambda model, i: pyo.quicksum(model.x[i, j] for j in model.J) == 1
        )
        self._model.single_crown_per_column_constraints = pyo.Constraint(
            self._model.J,
            rule=lambda model, j: pyo.quicksum(model.x[i, j] for i in model.I) == 1
        )
        self._model.single_crown_per_region_constraints = pyo.Constraint(
            self._model.K,
            rule=lambda model, k: pyo.quicksum(model.x[i, j] for (i, j) in model.R[k]) == 1
        )
        self._model.adjacent_squares_by_vertex_constraints = pyo.Constraint(
            self._model.D,
            rule=lambda model, i, j, r, s: model.x[i, j] + model.x[r, s] <= 1
        )
        return self
