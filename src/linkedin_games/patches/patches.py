from pprint import pprint

import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo

from ..core._game_board import GameBoard
from ._model import PatchesModel
from ._rectangle_seed import RectangleSeed


class Patches(GameBoard):
    """The LinkedIn Patches game, with colorful rectangles."""
    
    def __init__(self, board_dims:tuple[int, int], seeds: dict[tuple[int, int], dict[str, str|int]]) -> None:
        """
        Args:
            board_dims: Board dimensions as a `(rows, columns)` tuple.
            seeds: Rectangle seeds on board as a dictionary of
                `(row, column): {"color": color, "area": area, "shape": shape}`.
        """
        super().__init__(board_dims)
        self.__set_seeds(seeds)
        self._model = PatchesModel(self.board_dims, self.seeds)


    def __hash__(self) -> int:
        return hash((self._board_dims, self.__seeds))


    @property
    def seeds(self) -> dict[tuple[int, int], dict[str, str | int | None]]:
        """
        The seeds of the game.
        
        Returns:
            All the information about the seeds as a dictionary of
                `(row, column): {"color": color, "area": area, "shape": shape}`.
        """
        return {
            seed.square : {
                "color": self.color_code,
                "shape": self.shape,
                "area": self.area
            } for seed in self.__seeds
        }


    def __set_seeds(self, seeds: dict[tuple[int, int], dict[str, str|int]]) -> None:
        if not isinstance(seeds, dict):
            msg = f"seeds must be a dictionary. Got {type(seeds).__name__} instead."
            raise TypeError(msg)

        if len(seeds) < 1:
            msg = "seeds cannot be empty!"
            raise ValueError(msg)

        colors = [seed["color"] for seed in seeds.values()]
        if len(colors) != len(set(colors)):
            msg = "There must not be two or more seeds with the same color."
            raise ValueError(msg)

        self.__seeds = {
            RectangleSeed(
                color=seed.get("color"),
                square=square,
                area=seed.get("area"),
                shape=seed.get("shape")
            ) for square, seed in seeds.items()
        }


    @property
    def rectangles(self) -> dict[str, str | tuple[int, int]] | None:
        """
        All rectangles that solves the Patches game.

        Returns:
            The solving rectangles as a list of dictionaries as
                `{"color_code": color_code, "top_left": (top, left), "dims": (width, height)}`.
        """
        if not self.is_solved:
            return None
        return sorted([seed.rectangle for seed in self.__seeds], key=lambda x: x["top_left"])

    def _set_solution(self, verbose:bool = False) -> None:

        for seed in self.__seeds:
            top = round(pyo.value(self.model.t[seed.color_code]))
            left = round(pyo.value(self.model.l[seed.color_code]))
            width = round(pyo.value(self.model.w[seed.color_code]))
            height = round(pyo.value(self.model.h[seed.color_code]))
            seed.rectangle({
                "color": seed.color_code,
                "top": top,
                "left": left,
                "width": width,
                "height": height
            })
        
        nx.set_node_attributes(
            self.board,
            name="color",
            values={(i-1, j-1): seed.color_code for seed in self.__seeds for (i,j) in seed.rectangle.squares}
        )

        if verbose:
            print("These are the rectagles that solves the game:")
            pprint(self.solution)


    def show(self) -> None:
        """Show Patches' board."""
        plt.figure(figsize=(3, 3))
        nx.draw(
            self.board,
            pos={(i, j): (j, -i) for (i, j) in self.board.nodes()},
            node_size=1100,
            node_shape="s",
            node_color= list(nx.get_node_attributes(self.board, "color").values()),
            width=0
        )
        plt.show()
