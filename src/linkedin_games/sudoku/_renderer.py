import matplotlib.pyplot as plt
import networkx as nx

from .._shared.visualization.renderers._renderer import GameRenderer
from ._game_grid import SudokuGrid


class SudokuRenderer(GameRenderer[SudokuGrid]):

    def _set_grid(self) -> None:
        self._grid = nx.grid_2d_graph(*self._game.grid_dims)
        if self._game.solution:
            nx.set_node_attributes(
                self._grid,
                name="value",
                values={(i-1, j-1): k for (i, j), k in self._game.grid_squares.items()}
            )
        else:
            nx.set_node_attributes(self._grid, name="value", values=self._game.filled_squares)


    def show(self) -> None:
        """Show the Sudoku's grid."""
        plt.figure(figsize=(self._width, self._height))
        nx.draw(
            self._grid,
            pos= {(i, j): (j, -i) for (i, j) in self._grid.nodes()},
            with_labels= True,
            arrows=False,
            labels= {
                node: data.get("value")
                if data.get("value") is not None else ""
                for node, data in self._grid.nodes(data=True)
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
