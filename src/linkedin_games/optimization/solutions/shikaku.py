import pyomo.environ as pyo

from ._builder import GameSolutionBuilder


class ShikakuSolutionBuilder(GameSolutionBuilder):
    def _set_solution(self) -> None:
        self._solution.add(
            grid_squares={
                (i, j): k
                for (i, j) in self._opt_model.S for k in self._opt_model.K
                if round(pyo.value(self._opt_model.x[i, j, k])) == 1
            },
            rectangles={
                k: {
                    "top": round(pyo.value(self._opt_model.t[k])),
                    "left": round(pyo.value(self._opt_model.l[k])),
                    "height": round(pyo.value(self._opt_model.h[k])),
                    "width": round(pyo.value(self._opt_model.w[k]))
                } for k in self._opt_model.K
            }
        )
