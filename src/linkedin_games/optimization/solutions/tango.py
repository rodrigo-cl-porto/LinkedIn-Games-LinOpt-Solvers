import pyomo.environ as pyo

from ._builder import GameSolutionBuilder


class TangoSolutionBuilder(GameSolutionBuilder):
    def _set_solution(self) -> None:
        self._solution.add(
            grid_squares={
                (i, j): round(pyo.value(self._opt_model.x[i,j]))
                for i, j in self._opt_model.S
            }
        )
        squares = self._solution.get("grid_squares")
        self._solution.add(
            suns =[square for square, value in squares.items() if value == 0],
            moons=[square for square, value in squares.items() if value == 1],
        )
