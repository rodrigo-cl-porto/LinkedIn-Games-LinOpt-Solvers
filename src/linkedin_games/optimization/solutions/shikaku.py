import pyomo.environ as pyo

from ...domain.games.shikaku._rectangle import Rectangle
from ._builder import GameSolutionBuilder


class ShikakuSolutionBuilder(GameSolutionBuilder):
    def _set_solution(self) -> None:
        self._solution.add(
            grid_squares={
                (i, j): k for (i, j) in self._model.S for k in self._model.K
                if round(pyo.value(self._model.x[i, j, k])) == 1
            },
            rectangles={
                k: Rectangle(
                    (
                        round(pyo.value(self._model.t[k])),
                        round(pyo.value(self._model.l[k]))
                    ),
                    (
                        round(pyo.value(self._model.h[k])),
                        round(pyo.value(self._model.w[k]))
                    )
                ) for k in self._model.K
            }
        )
