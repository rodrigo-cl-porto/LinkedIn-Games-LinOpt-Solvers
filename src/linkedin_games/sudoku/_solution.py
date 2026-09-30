from typing import TYPE_CHECKING, Self, cast

import pyomo.environ as pyo

from .._shared.optimization.solution._solution import GameSolution

if TYPE_CHECKING:
    from collections.abc import Iterable


class SudokuSolution(GameSolution):

    def build(self, opt_model: pyo.ConcreteModel) -> Self:
        return super().build(opt_model)


    def _set_squares(self) -> None:
        digits = cast("Iterable[int]", self._model.K)
        squares = cast("Iterable[tuple[int, int]]", self._model.S)
        x = cast("pyo.Var", self._model.x)
        self._squares={
            (i, j): k for (i, j) in squares for k in digits
            if round(pyo.value(x[i, j, k])) == 1
        }
