import matplotlib.pyplot as plt
import networkx as nx

from ...domain.games.zip.zip import Zip
from ._renderer import GameRenderer


class ZipRenderer(GameRenderer[Zip]):

    def show(self, game: Zip) -> None:
        E = self.model.E
        N = self.model.N
        K = self.model.K
        x = self.model.x

        width = height = self.size * 0.7
        plt.figure(figsize=(width, height))
        path_color = super()._generate_hex_code()
        labels = {N.at(k): k for k in K}
        labels = {(i-1, j-1): k for (i,j), k in labels.items()}
        pos={(i,j): (j,-i) for i, j in self.grid.nodes()}

        if self.walls is not None:
            walls = nx.draw_networkx_edges(
                self.grid,
                pos=pos,
                edgelist=[((i-1, j-1), (r-1, s-1)) for (i,j),(r,s) in self.walls],
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
            node_shape="o" if self.is_solved else "s",
            node_size= 800,
            node_color= [
                "white" if (i+1,j+1) in self.numbered_squares else path_color
                for (i,j) in self.grid.nodes()
            ],
            edge_color= path_color,
            edgecolors= path_color,
            linewidths= 1,
            width= 30,
            edgelist= [
                ((i-1, j-1), (r-1, s-1)) for i,j,r,s in E
                if round(pyo.value(x[i, j, r, s])) == 1
            ]
        )

        plt.show()
