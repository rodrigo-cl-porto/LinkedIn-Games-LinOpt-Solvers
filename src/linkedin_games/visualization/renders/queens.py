import matplotlib.pyplot as plt
import networkx as nx

from ...domain.games.queens.queens import Queens
from ._renderer import GameRenderer


class QueensRenderer(GameRenderer[Queens]):

    def render(self, game: Queens) -> None:
        """Show the Queens' grid."""
        plt.figure(figsize=(self._width, self._height))
        nx.draw(
            game.grid,
            pos={(i, j): (j, -i) for i, j in game.grid.nodes()},
            with_labels=True,
            arrows=False,
            labels=dict.fromkeys(game.__crowns.nodes(), "O") if self.__crowns is not None else dict.fromkeys(self.grid.nodes(), ""),
            node_size=1100,
            node_color=list(nx.get_node_attributes(self.grid, "color").values()),
            node_shape="s", # Squared-shape nodes
            width=0,
            edgecolors="black",
            linewidths=.5
        )
        plt.show()
