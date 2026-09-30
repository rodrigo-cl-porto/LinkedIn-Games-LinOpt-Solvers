import matplotlib.pyplot as plt
import networkx as nx

from .._shared.visualization._renderer import GameRenderer
from ._game_grid import SudokuGrid


class SudokuRenderer(GameRenderer[SudokuGrid]):

    def _set_grid(self) -> None:
        super()._set_grid()

    def display(self) -> None:
        plt.figure(figsize=(self._width, self._height))
        nx.draw(
            self._grid,
            pos= {(i, j): (j, -i) for (i, j) in self._grid.nodes()},
            with_labels= True,
            arrows=False,
            labels= {
                (i-1, j-1): digit if digit else ""
                for (i,j), digit in self._game.squares.items()
            },
            font_color="white",
            node_size= 1100,
            node_shape="s",
            node_color= "#1B1F22",
            width= 0,
            edgecolors="#999999",
            linewidths= 1,
        )
        plt.show()
