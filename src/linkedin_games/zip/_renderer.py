import matplotlib.pyplot as plt
import networkx as nx

from .._shared.utils.color_generator import ColorGenerator
from .._shared.visualization._renderer import GameRenderer
from ._game_grid import ZipGrid


class ZipRenderer(GameRenderer[ZipGrid]):
    _SCALE_FACTOR = .7

    def _set_grid(self) -> None:
        super()._set_grid()
        nx.set_edge_attributes(
            self._grid,
            name="value",
            values={((i-1, j-1), (r-1, s-1)): k for ((i, j), (r, s)), k in self._game.edges.items()}
        )

    def display(self) -> None:
        plt.figure(figsize=(self._width, self._height))
        path_color = ColorGenerator.generate_hex_code()
        labels = {
            (i-1, j-1): k+1
            for k, (i,j) in enumerate(self._game.numbered_squares)
        }
        pos= {(i,j): (j,-i) for i, j in self._grid.nodes()}

        if self._game.walls != []:
            walls = nx.draw_networkx_edges(
                self._grid,
                pos=pos,
                edgelist=[((i-1, j-1), (r-1, s-1)) for (i,j), (r,s) in self._game.walls],
                edge_color="#000000",
                hide_ticks=True,
                arrows=False,
                width=30,
            )
            walls.set_zorder(0)

        squares = nx.draw_networkx_nodes(
            self._grid,
            pos= pos,
            node_shape="s",
            node_size= 1100,
            node_color= "#FFFFFF",
            linewidths= 2,
        )
        squares.set_zorder(1)

        nx.draw( # Drawing the path
            self._grid,
            pos= pos,
            with_labels= True,
            labels=labels,
            arrows=False,
            node_shape="o" if self._game.is_solved else "s",
            node_size= 800,
            node_color= [
                "white" if (i,j) in self._game.numbered_squares else path_color
                for (i,j) in self._game.squares
            ],
            edge_color= path_color,
            edgecolors= path_color,
            linewidths= 1,
            width= 30,
            edgelist= [
                ((i-1, j-1), (r-1, s-1))
                for ((i,j), (r,s)), value in self._game.edges.items()
                if value == 1
            ]
        )

        plt.show()
