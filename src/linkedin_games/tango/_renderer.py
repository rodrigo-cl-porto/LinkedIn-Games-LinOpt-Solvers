import matplotlib.pyplot as plt
import networkx as nx

from .._shared.visualization.renderer.renderer import GameRenderer
from ._game_grid import TangoGrid


class TangoRenderer(GameRenderer[TangoGrid]):

    def _set_grid(self) -> None:
        super()._set_grid()

    def display(self) -> None:
        """Show Tango's grid."""
        pos = {(i, j): (j, -i) for i, j in self._grid.nodes()}
        nx.draw(
            self._grid,
            pos= pos,
            arrows=False,
            with_labels= True,
            labels= {
                (i-1, j-1): value if value is not None else ""
                for (i, j), value in self._game.squares.items()
            },
            node_size= 1100,
            node_color= [
                "#EEEAE7" if (i+1,j+1) in self._game.filled_squares else "#FFFFFF"
                for (i, j) in self._grid.nodes()
            ],
            node_shape="s",
            edgecolors="#EEEAE7",
            linewidths=1,
            width=0,
            edgelist=
                [((i-1, j-1), (r-1, s-1)) for ((i, j), (r, s)) in self._game.opposite_pairs] +
                [((i-1, j-1), (r-1, s-1)) for ((i, j), (r, s)) in self._game.matching_pairs]
        )
        nx.draw_networkx_edge_labels(
            self._grid,
            pos= pos,
            edge_labels=
                {((i-1, j-1), (r-1, s-1)): "×" for ((i, j), (r, s)) in self._game.opposite_pairs} |
                {((i-1, j-1), (r-1, s-1)): "=" for ((i, j), (r, s)) in self._game.matching_pairs},
            font_color="#887658"
        )
        plt.show()
