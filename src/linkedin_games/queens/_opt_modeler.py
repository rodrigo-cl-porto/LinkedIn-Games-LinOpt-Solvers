import pyomo.environ as pyo

from .._shared.optimization.modeler.opt_modeler import OptModeler
from ._game_grid import QueensGrid


class QueensOptModeler(OptModeler[QueensGrid]):

    def _set_range_sets(self) -> None:
        super()._set_range_sets()
        self._model.K = pyo.Set(initialize=self._game.regions.keys()) # Colored Regions

    def _set_composite_sets(self) -> None:
        super()._set_composite_sets()
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

    def _set_parameters(self) -> None:
        super()._set_parameters()

    def _set_decision_variables(self) -> None:
        self._model.x = pyo.Var(self._model.S, domain=pyo.Binary, initialize=0)

    def _set_objective_function(self) -> None:
        self._model.obj = pyo.Objective(expr=0) # feasibility problem

    def _set_constraints(self) -> None:
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
