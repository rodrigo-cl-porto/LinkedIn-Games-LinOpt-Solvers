import pyomo.environ as pyo

from ._builder import GameSolutionBuilder


class SudokuSolutionBuilder(GameSolutionBuilder):
    def _set_solution(self) -> None:
        self._solution.add(grid_squares={
            (i, j): k
            for (i, j) in self._opt_model.S for k in self._opt_model.K
            if round(pyo.value(self._opt_model.x[i,j,k])) == 1
        })
