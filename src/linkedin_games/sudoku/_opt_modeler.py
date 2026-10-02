import pyomo.environ as pyo

from .._shared.optimization.modeler.opt_modeler import OptModeler
from ._game_grid import SudokuGrid


class SudokuOptModeler(OptModeler[SudokuGrid]):

    def _set_board_dimensions(self) -> None:
        super()._set_board_dimensions()
        p, q = self._game.block_dims
        self._model.p = pyo.Param(initialize=p, domain=pyo.PositiveIntegers)
        self._model.q = pyo.Param(initialize=q, domain=pyo.PositiveIntegers)

    def _set_range_sets(self) -> None:
        super()._set_range_sets()
        self._model.K = pyo.RangeSet(self._model.n) # Digits
        self._model.U = pyo.RangeSet(self._model.p) # Rows per block
        self._model.V = pyo.RangeSet(self._model.q) # Columns per block

    def _set_composite_sets(self) -> None:
        super()._set_composite_sets()
        self._model.B = pyo.Set( # Grid blocks
            self._model.V, self._model.U,
            initialize= lambda model, v, u: [
                (i, j)
                for i in range(model.p*(v-1) + 1, model.p*v + 1)
                for j in range(model.q*(u-1) + 1, model.q*u + 1)
            ],
            domain=self._model.S
        )
        self._model.F = pyo.Set( # Filled values
            initialize=((i, j, k) for (i,j), k in self._game.filled_squares.items()),
            dimen=3
        )

    def _set_parameters(self) -> None:
        super()._set_parameters()

    def _set_decision_variables(self) -> None:
        self._model.x = pyo.Var(
            self._model.S, self._model.K,
            domain=pyo.Binary,
            initialize=0
        )

    def _set_objective_function(self) -> None:
        self._model.obj = pyo.Objective(expr=0) # feasibility problem

    def _set_constraints(self) -> None:
        self._model.unique_digits_per_row_constraints = pyo.Constraint(
            self._model.J, self._model.K,
            rule=lambda model, j, k: pyo.quicksum(model.x[i,j,k] for i in model.I) == 1
        )
        self._model.unique_digits_per_column_constraints = pyo.Constraint(
            self._model.I, self._model.K,
            rule=lambda model, i, k: pyo.quicksum(model.x[i,j,k] for j in model.J) == 1
        )
        self._model.unique_digits_per_block_constraints = pyo.Constraint(
            self._model.V, self._model.U, self._model.K,
            rule=lambda model, v, u, k: pyo.quicksum(model.x[i,j,k] for (i, j) in model.B[v,u]) == 1
        )
        self._model.single_digit_per_square_constraints = pyo.Constraint(
            self._model.S,
            rule=lambda model, i, j: pyo.quicksum(model.x[i,j,k] for k in model.K) == 1
        )
        self._model.alreadey_filled_squares_constraints = pyo.Constraint(
            self._model.F,
            rule=lambda model, i, j, k: model.x[i,j,k] == 1
        )
