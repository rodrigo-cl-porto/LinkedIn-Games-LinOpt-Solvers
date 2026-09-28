import pyomo.environ as pyo

from ._builder import GameSolutionBuilder


class ZipSolutionBuilder(GameSolutionBuilder):
    def _set_solution(self) -> None:
        self._solution.add(
            grid_squares = {
                (i, j): round(pyo.value(self._model.u[i,j]))
                for i, j in self._model.S
            },
            grid_edges = {
                ((i,j), (r,s)): round(pyo.value(self._model.x[i,j,r,s]))
                for i, j, r, s in self._model.E
            }
        )
