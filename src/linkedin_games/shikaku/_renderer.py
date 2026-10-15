import matplotlib.pyplot as plt
import networkx as nx

from .._shared.visualization.renderer.renderer import GameRenderer
from ._game_grid import ShikakuGrid


class ShikakuRenderer(GameRenderer[ShikakuGrid]):

    def _set_grid(self) -> None:
        self._grid = nx.grid_2d_graph(*self._game.dims)
        nx.set_node_attributes(
            self._grid,
            name="color",
            values={(i-1, j-1): k for (i, j), k in self._game.squares.items()}
        )
        nx.set_node_attributes(
            self._grid,
            name="seed_area",
            values={
                tuple(i-1 for i in seed["square"]): seed["area"]
                for seed in self._game.seeds.values()
            }
        )

    def display(self) -> None:
        plt.figure(figsize=(self._width, self._height))
        nx.draw(
            self._grid,
            pos={(i, j): (j, -i) for (i, j) in self._grid.nodes()},
            with_labels=True,
            labels= {
                tuple(i-1 for i in seed["square"]): seed["area"] if seed.get("area") else ""
                for seed in self._game.seeds.values()
            },
            node_size=1100,
            node_shape="s",
            node_color= list(nx.get_node_attributes(self._grid, "color").values()),
            width=0,
            arrows=False,
            edgecolors="black",
            linewidths=1
        )
        plt.show()
