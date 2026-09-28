import matplotlib.pyplot as plt
import networkx as nx

from ...domain.games.shikaku.shikaku import Shikaku
from ._renderer import GameRenderer


class ShikakuRenderer(GameRenderer[Shikaku]):

    def _set_grid(self) -> None:
        self._grid = nx.grid_2d_graph(*self._game.grid_dims)
        if not self._game.solution:
            nx.set_node_attributes(self._grid, "#FFFFFF", name="value")
            nx.set_node_attributes( # Adding a color for each square on the grid
                self._grid,
                name="value",
                values={
                    tuple(i-1 for i in seed["square"]): seed["color"]
                    for seed in self._game.seeds.values()
                }
            )
        else:
            nx.set_node_attributes(
                self._grid,
                name="value",
                values={(i-1, j-1): k for (i, j), k in self._game.grid_squares.items()}
            )


    def show(self) -> None:
        plt.figure(figsize=(self._width, self._height))
        nx.draw(
            self.grid,
            pos={(i, j): (j, -i) for (i, j) in self._grid.nodes()},
            node_size=1100,
            node_shape="s",
            node_color= list(nx.get_node_attributes(self._grid, "value").values()),
            width=0,
            arrows=False,
            edgecolors="black",
            linewidths=1
        )
        plt.show()
