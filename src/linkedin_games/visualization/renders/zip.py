import matplotlib.pyplot as plt
import networkx as nx

from ...domain.games.zip.zip import Zip
from ...domain.utils.color_generator import ColorGenerator
from ._renderer import GameRenderer


class ZipRenderer(GameRenderer[Zip]):

    _SCALE_FACTOR = .7

    def _set_grid(self) -> None:
        self._grid = nx.grid_2d_graph(*self._game.grid_dims).to_directed()
        if self._game.solution:
            nx.set_node_attributes(
                self._grid,
                name="value",
                values={(i-1, j-1): k for (i, j), k in self._game.grid_squares.items()}
            )
            nx.set_edge_attributes(
                self._grid,
                name="value",
                values={((i-1, j-1), (r-1, s-1)): k for ((i, j), (r, s)), k in self._game.grid_edges.items()}
            )
        else:
            nx.set_node_attributes(
                self.grid,
                name="value",
                values= {square: index for index, square in enumerate(self._game.numbered_squares)}
            )
            nx.set_edge_attributes(self._grid, name="value", values=None)


    def show(self) -> None:
        plt.figure(figsize=(self._width, self._height))
        path_color = ColorGenerator.generate_hex_code()
        labels = {
            (i-1, j-1): k
            for k, (i, j) in enumerate(self._game.numbered_squares)
        }
        pos= {(i,j): (j,-i) for i, j in self.grid.nodes()}

        if self._game.walls is not None:
            walls = nx.draw_networkx_edges(
                self.grid,
                pos=pos,
                edgelist=[((i-1, j-1), (r-1, s-1)) for (i,j), (r,s) in self._game.walls],
                edge_color="#000000",
                hide_ticks=True,
                arrows=False,
                width=30
            )
            walls.set_zorder(0)

        grid_squares = nx.draw_networkx_nodes(
            self.grid,
            pos= pos,
            node_shape="s",
            node_size= 1100,
            node_color= "#FFFFFF",
            linewidths= 2,
        )
        grid_squares.set_zorder(1)

        nx.draw( # Drawing the path
            self.grid,
            pos= pos,
            with_labels= True,
            labels=labels,
            arrows=False,
            node_shape="o" if self._game.solution else "s",
            node_size= 800,
            node_color= [
                "white" if (i+1,j+1) in self._game.numbered_squares else path_color
                for (i,j) in self.grid.nodes()
            ],
            edge_color= path_color,
            edgecolors= path_color,
            linewidths= 1,
            width= 30,
            edgelist= [
                ((i-1, j-1), (r-1, s-1))
                for ((i,j), (r,s)), value in self._game.grid_edges.items()
                if value == 1
            ]
        )

        plt.show()
