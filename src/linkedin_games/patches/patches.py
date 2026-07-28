from pprint import pprint

import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo

from linkedin_games.patches._model import PatchesModel

from ..core._game_board import GameBoard
from ._rectangle import Rectangle
from ._seed_square import SeedSquare


class Patches(GameBoard):
    """A Patches board game with colorful rectangles.

    Attributes:
        board_dims (tuple[int, int]): The dimensions of the board as (rows, columns).
        seeds (tuple[SeedSquare]): All the seeds of the game.

    Methods:
        _construct_model (None): Construct the linear optimization model for the Patches game.
        _set_solution (None): Set the solution of the Patches game.
        _show (None): Show the Patches game board with rectangles.
    """
    def __init__(self, board_dims:tuple[int, int], seeds:dict[tuple[int, int], dict[str, str|int]]) -> None:
        """
        Args:
            board_dims (tuple[int, int]): The dimensions of the board as (rows, columns).
            seeds (tuple[SeedSquare]): The seeds of the game.
        """
        super().__init__(board_dims)
        self.__set_seeds(seeds)
        self._model = PatchesModel(self.board_dims, self.seeds)


    def __hash__(self) -> int:
        return hash((self.board_dims, self.seeds))


    @property
    def seeds(self) -> set[SeedSquare]:
        """tuple[SeedSquare]: All the seeds of the game."""
        return self.__seeds

    def __set_seeds(self, seeds:dict[tuple[int, int], dict[str, str|int]]) -> None:
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
            SeedSquare(
                square=square,
                area=seed.get("area"),
                shape=seed.get("shape"),
                color=seed.get("color")
            ) for square, seed in seeds.items()
        }


    @property
    def rectangles(self) -> list[Rectangle] | None:
        return self.solution

    @property
    def solution(self) -> list[Rectangle] | None:
        """All the rectangles of the Patches game."""
        if not self.is_solved:
            return None
        return sorted([seed.rectangle.to_dict() for seed in self.seeds], key=lambda x: x["top_left_square"])

    def _set_solution(self, verbose:bool = False) -> None:
        for seed in self.seeds:
            top = round(pyo.value(self.model.t[seed.color_code]))
            left = round(pyo.value(self.model.l[seed.color_code]))
            width = round(pyo.value(self.model.w[seed.color_code]))
            height = round(pyo.value(self.model.h[seed.color_code]))
            seed._set_rectangle(
                Rectangle(
                    color=seed.color_code,
                    top_left_square=(top, left),
                    dims=(width, height),
                )
            )
        nx.set_node_attributes(
            self.board,
            name="color",
            values={(i - 1, j - 1): seed.color_code for seed in self.seeds for (i, j) in seed.rectangle.squares}
        )
        if verbose:
            print("These are the rectagles that solves the game:")
            pprint(self.solution)


    def show(self) -> None:
        plt.figure(figsize=(3, 3))
        nx.draw(
            self.board,
            pos={(i, j): (j, -i) for (i, j) in self.board.nodes()},
            node_size=1100,
            node_shape="s",
            node_color=[
                color for color in nx.get_node_attributes(self.board, "color").values()
            ],
            width=0
        )
        plt.show()
