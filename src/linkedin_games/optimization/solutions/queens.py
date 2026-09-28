import pyomo.environ as pyo

from ._builder import GameSolutionBuilder


class QueensSolutionBuilder(GameSolutionBuilder):
    def _set_solution(self) -> None:
        self._solution.add(grid_squares={
            (i, j): round(pyo.value(self._model.x[i,j]))
            for i, j in self._model.S
        })
