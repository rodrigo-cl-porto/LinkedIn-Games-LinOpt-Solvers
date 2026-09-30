from typing import TYPE_CHECKING, Self, cast

import pyomo.environ as pyo

from .._shared.optimization.solution._solution import GameSolution

if TYPE_CHECKING:
    from collections.abc import Iterable


class QueensSolution(GameSolution):

    def build(self, opt_model: pyo.ConcreteModel) -> Self:
        return super().build(opt_model)


    def _set_grid_squares(self) -> None:
        squares = cast("Iterable[tuple[int, int]]", self._model.S)
        x = cast("pyo.Var", self._model.x)
        self._grid_squares = {
            (i, j): round(pyo.value(x[i,j]))
            for i, j in squares
        }


    @property
    def crowns(self) -> list[tuple[int, int]]:
        return [square for square, value in self._grid_squares.items() if value == 1]
