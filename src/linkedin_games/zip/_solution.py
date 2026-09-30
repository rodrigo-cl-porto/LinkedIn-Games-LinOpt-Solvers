from typing import TYPE_CHECKING, Self, cast

import pyomo.environ as pyo

from .._shared.optimization.solution._solution import GameSolution

if TYPE_CHECKING:
    from collections.abc import Iterable


class ZipSolution(GameSolution):

    def build(self, opt_model: pyo.ConcreteModel) -> Self:
        super().build(opt_model)
        self._set_edges()
        return self

    def _set_squares(self) -> None:
        squares = cast("Iterable[tuple[int, int]]", self._model.S)
        u = cast("pyo.Var", self._model.u)
        self._squares = {
            (i, j): round(pyo.value(u[i, j]))
            for i, j in squares
        }

    @property
    def edges(self) -> dict[tuple[tuple[int, int], tuple[int, int]], int]:
        return self._edges

    def _set_edges(self) -> None:
        edges = cast("Iterable[tuple[int, int, int, int]]", self._model.E)
        x = cast("pyo.Var", self._model.x)
        self._edges = {
            ((i, j), (r, s)): round(pyo.value(x[i, j, r, s]))
            for i, j, r, s in edges
        }

    @property
    def path(self) -> list[tuple[int, int]]:
        return sorted(
            self._squares,
            key=lambda square: self._squares[square] or 0,
        )
