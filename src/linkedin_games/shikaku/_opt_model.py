import pyomo.environ as pyo

from .._shared.optimization.models.builder import OptimizationModelBuilder
from ._game_grid import ShikakuGrid


class ShikakuModelBuilder(OptimizationModelBuilder[ShikakuGrid]):

    def _set_range_sets(self) -> None:
        super()._set_range_sets()
        self._model.K = pyo.Set(initialize=(seed["color_code"] for seed in self._game.seeds.values())) # Rectangles


    def _set_composite_sets(self) -> None:
        super()._set_composite_sets()
        self._model.E = pyo.Set( # Rectangle Seeds
            initialize=[(*seed["square"], seed["color_code"]) for seed in self._game.seeds.values()]
        )
        self._model.A = pyo.Set( # Rectangles with required area
            initialize=[seed["color_code"] for seed in self._game.seeds.values() if seed["area"] is not None],
            domain=self._model.K
        )


    def _set_decision_variables(self) -> None:
        self.__set_rectangle_shape_decision_variables()
        self.__set_grid_square_decision_variables()


    def __set_rectangle_shape_decision_variables(self) -> None:
        self._model.t = pyo.Var( # Index of the top row of the rectangle k
            self._model.K,
            domain=pyo.PositiveIntegers,
            initialize=1,
            bounds=(1, self._model.m)
        )
        self._model.l = self.l = pyo.Var( # Index of the leftmost column of the rectangle k
            self._model.K,
            domain=pyo.PositiveIntegers,
            initialize=1,
            bounds=(1, self._model.n)
        )
        self._model.h = pyo.Var( # Height of rectangle k
            self._model.K,
            domain=pyo.PositiveIntegers,
            initialize=1,
            bounds=(1, self._model.m)
        )
        self._model.w = pyo.Var( # Width of rectangle k
            self._model.K,
            domain=pyo.PositiveIntegers,
            initialize=1,
            bounds=(1, self._model.n)
        )


    def __set_grid_square_decision_variables(self) -> None:
        self._model.u = pyo.Var( # u_ik = 1 if row i passes through rectangle k
            self._model.I, self._model.K,
            domain=pyo.Binary,
            initialize=0
        )
        self._model.v = pyo.Var( # v_jk = 1 if column j passes through rect k
            self._model.J, self._model.K,
            domain=pyo.Binary,
            initialize=0
        )
        self._model.x = pyo.Var( # x_ijk = 1 if square (i,j) is covered by rect k
            self._model.I, self._model.J, self._model.K,
            domain=pyo.Binary,
            initialize=0
        )


    def _set_parameters(self) -> None:
        self._model.a = pyo.Param( # Required areas
            self._model.K,
            domain=pyo.PositiveIntegers,
            initialize={
                seed["color_code"]: seed["area"]
                for seed in self._game.seeds.values() if seed["area"] is not None
            }
        )


    def _set_objective_function(self) -> None:
        self._model.obj = pyo.Objective(expr=0) # feasibility problem


    def _set_constraints(self) -> None:
        self._set_non_overlapping_rectangles_constraints()
        self._set_game_grid_boundaries_constraints()
        self._set_rectangle_boundaries_constraints()
        self._set_rectangle_dimensions_constraints()
        self._set_mccormick_linearization_constraints()
        self._set_rectangle_seed_constraints()


    def _set_non_overlapping_rectangles_constraints(self) -> None:
        self.unique_rectangle_per_square_constraints = pyo.Constraint(
            self._model.S,
            rule=lambda model, i, j: pyo.quicksum(model.x[i, j, k] for k in model.K) == 1
        )


    def _set_game_grid_boundaries_constraints(self) -> None:
        self._model.bottom_row_constraints = pyo.Constraint(
            self._model.K,
            rule=lambda model, k: model.t[k] + model.h[k] - 1 <= model.m
        )
        self._model.rightmost_column_constraints = pyo.Constraint(
            self._model.K,
            rule=lambda model, k: model.l[k] + model.w[k] - 1 <= model.n
        )


    def _set_rectangle_boundaries_constraints(self) -> None:
        self._model.top_boundary_constraints = pyo.Constraint(
            self._model.I, self._model.K,
            rule=lambda model, i, k: model.t[k] - i <= model.m * (1 - model.u[i,k])
        )
        self._model.bottom_boundary_constraints = pyo.Constraint(
            self._model.I, self._model.K,
            rule=lambda model, i, k: i - (model.t[k] + model.h[k] - 1) <= model.m * (1 - model.u[i,k])
        )
        self._model.left_boundary_constraints = pyo.Constraint(
            self._model.J, self._model.K,
            rule=lambda model, j, k: model.l[k] - j <= model.n * (1 - model.v[j,k])
        )
        self._model.right_boundary_constraints = pyo.Constraint(
            self._model.J, self._model.K,
            rule=lambda model, j, k: j - (model.l[k] + model.w[k] - 1) <= model.n * (1 - model.v[j,k])
        )


    def _set_rectangle_dimensions_constraints(self) -> None:
        self._model.height_constraints = pyo.Constraint(
            self._model.K,
            rule=lambda model, k: pyo.quicksum(model.u[i,k] for i in model.I) == model.h[k]
        )
        self._model.width_constraints = pyo.Constraint(
            self._model.K,
            rule=lambda model, k: pyo.quicksum(model.v[j,k] for j in model.J) == model.w[k]
        )


    def _set_mccormick_linearization_constraints(self) -> None:
        self._model.cutout_row_constraints = pyo.Constraint(
            self._model.I, self._model.K,
            rule=lambda model, i, k: pyo.quicksum(model.x[i,j,k] for j in model.J) <= model.n * model.u[i,k]
        )
        self._model.cutout_column_constraints = pyo.Constraint(
            self._model.J, self._model.K,
            rule=lambda model, j, k: pyo.quicksum(model.x[i,j,k] for i in model.I) <= model.m * model.v[j,k]
        )
        self._model.square_coverage_constraints = pyo.Constraint(
            self._model.I, self._model.J, self._model.K,
            rule=lambda model, i, j, k: model.x[i,j,k] >= model.u[i,k] + model.v[j,k] - 1
        )


    def _set_rectangle_seed_constraints(self) -> None:
        self._model.seed_square_constraints = pyo.Constraint(
            self._model.E,
            rule=lambda model, i, j, k: model.x[i,j,k] == 1
        )
        self._model.area_constraints = pyo.Constraint( # Required areas
            self._model.A,
            rule=lambda model, k: pyo.quicksum(model.x[i, j, k] for (i, j) in model.S) == model.a[k]
        )
