

from typing import TYPE_CHECKING, Self, cast

import pyomo.environ as pyo

from .._shared.optimization.solution._solution import GameSolution
from ._rectangle import Rectangle

if TYPE_CHECKING:
    from collections.abc import Iterable


class ShikakuSolution(GameSolution):

    def build(self, opt_model: pyo.ConcreteModel) -> Self:
        super().build(opt_model)
        self._set_rectangles()
        return self

    def _set_squares(self) -> None:
        colors = cast("Iterable[str]", self._model.K)
        squares = cast("Iterable[tuple[int, int]]", self._model.S)
        x = cast("pyo.Var", self._model.x)
        self._squares={
            (i, j): k for (i, j) in squares for k in colors
            if round(pyo.value(x[i, j, k])) == 1
        }

    @property
    def rectangles(self) -> dict[str, Rectangle]:
        return self._rectangles

    def _set_rectangles(self) -> None:
        seed_colors = cast("Iterable[str]", self._model.K)
        top = cast("pyo.Var", self._model.t)
        left = cast("pyo.Var", self._model.l)
        height = cast("pyo.Var", self._model.h)
        width = cast("pyo.Var", self._model.w)
        self._rectangles = {
            k: Rectangle(
                (
                    round(pyo.value(top[k])),
                    round(pyo.value(left[k]))
                ),
                (
                    round(pyo.value(height[k])),
                    round(pyo.value(width[k]))
                )
            ) for k in seed_colors
        }
