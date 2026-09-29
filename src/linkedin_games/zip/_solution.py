from typing import TYPE_CHECKING, Self, cast

import pyomo.environ as pyo

from .._shared.optimization.solutions._solution import GameSolution

if TYPE_CHECKING:
    from collections.abc import Iterable


class ZipSolution(GameSolution):

    def build(self, opt_model: pyo.ConcreteModel) -> Self:
        super().build(opt_model)
        self._set_grid_edges()
        return self


    def _set_grid_squares(self) -> None:
        squares = cast("Iterable[tuple[int, int]]", self._model.S)
        u = cast("pyo.Var", self._model.u)
        self._grid_squares = {
            (i, j): round(pyo.value(u[i, j]))
            for i, j in squares
        }


    @property
    def grid_edges(self) -> dict[tuple[tuple[int, int], tuple[int, int]], int]:
        return self._grid_edges


    def _set_grid_edges(self) -> None:
        edges = cast("Iterable[tuple[int, int, int, int]]", self._model.E)
        x = cast("pyo.Var", self._model.x)
        self._grid_edges = {
            ((i, j), (r, s)): round(pyo.value(x[i, j, r, s]))
            for i, j, r, s in edges
        }


    @property
    def path(self) -> list[tuple[int, int]]:
        return sorted(
            self._grid_squares,
            key=lambda square: self._grid_squares[square] or 0,
        )
