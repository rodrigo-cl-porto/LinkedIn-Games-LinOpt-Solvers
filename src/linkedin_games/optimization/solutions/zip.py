import pyomo.environ as pyo

from ._builder import GameSolutionBuilder


class ZipSolutionBuilder(GameSolutionBuilder):
    def _set_solution(self) -> None:
        self._solution.add(
            grid_squares = {
                (i, j): round(pyo.value(self._opt_model.u[i,j]))
                for i, j in self._opt_model.S
            },
            grid_edges = {
                ((i,j), (r,s)): round(pyo.value(self._opt_model.x[i,j,r,s]))
                for i, j, r, s in self._opt_model.E
            }
        )
        squares = self._solution.get("grid_squares")
        self._solution.add(path=sorted(squares.keys(), key=squares.get))
