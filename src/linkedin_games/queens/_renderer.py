import matplotlib.pyplot as plt
import networkx as nx

from .._shared.visualization.renderers._renderer import GameRenderer
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


    def show(self) -> None:
        """Show the Queens' grid."""
        plt.figure(figsize=(self._width, self._height))
        nx.draw(
            self._grid,
            pos={(i, j): (j, -i) for i, j in self._grid.nodes()},
            with_labels=True,
            arrows=False,
            labels=dict.fromkeys(self._game.crowns, "O") if self._game.crowns != [] else None,
            node_size=1100,
            node_color=list(nx.get_node_attributes(self.grid, "color").values()),
            node_shape="s", # Squared-shape nodes
            width=0,
            edgecolors="black",
            linewidths=.5
        )
        plt.show()
