import matplotlib.pyplot as plt
import networkx as nx

from .._shared.visualization.renderer.renderer import GameRenderer
from ._game_grid import QueensGrid


class QueensRenderer(GameRenderer[QueensGrid]):

    def _set_grid(self) -> None:
        super()._set_grid()
        nx.set_node_attributes( # Adding a color for each square on the grid
            self._grid,
            name="color",
            values={
                (i-1, j-1): color_code
                for color_code, squares in self._game.regions.items()
                for (i, j) in squares
            }
        )

    def display(self) -> None:
        plt.figure(figsize=(self._width, self._height))
        nx.draw(
            self._grid,
            pos={(i, j): (j, -i) for i, j in self._grid.nodes()},
            with_labels=True,
            arrows=False,
            labels={
                (i-1, j-1): "" if not value else "O" if value == 1 else ""
                for (i, j), value in self._game.squares.items()
            },
            node_size=1100,
            node_color=list(nx.get_node_attributes(self._grid, "color").values()),
            node_shape="s", # Squared-shape nodes
            width=0,
            edgecolors="black",
            linewidths=.5
        )
        plt.show()
