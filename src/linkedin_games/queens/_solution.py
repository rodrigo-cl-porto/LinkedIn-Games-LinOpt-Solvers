from typing import TYPE_CHECKING, Self, cast

import pyomo.environ as pyo

from .._shared.optimization.solution.solution import GameSolution

if TYPE_CHECKING:
    from collections.abc import Iterable


class QueensSolution(GameSolution):

    def build(self, opt_model: pyo.ConcreteModel) -> Self:
        return super().build(opt_model)

    def _set_squares(self) -> None:
        squares = cast("Iterable[tuple[int, int]]", self._model.S)
        x: pyo.Var = cast("pyo.Var", self._model.x)
        self._squares = {
            (i, j): round(pyo.value(x[i,j]))
            for i, j in squares
        }
