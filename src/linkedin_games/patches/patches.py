from pprint import pprint

import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo

from ..core._color_generator_mixin import ColorGeneratorMixin
from ..core._game_board import GameBoard
from ._model import PatchesModel
from ._rectangle_seed import RectangleSeed


class Patches(ColorGeneratorMixin, GameBoard):
    """
    The [LinkedIn Patches](https://www.linkedin.com/games/patches/) game.
    
    A game board with some colored rectangle seeds that may state some features about the rectangles
        to be built on the board, such as a required area (optional) or a required shape
        (which can be a `vertical` rectangle, a `horizontal` rectangle, a `square` or any shape).

    Objective:
        Partition the board into non-overlapping rectangular patches so that each patch meets
        the prescriptions on their respective seeds.
    
    Rules:
        - Each seed must be covered by only one rectangle that attends its prescriptions;
        - A rectangle must cover only one seed;
        - The area of all rectangles must be greater than 1 square on the board.
    """

    def __init__(self, size:int, seeds: dict[tuple[int, int], dict[str, str | int | None] | None]) -> object:
        """
        Args:
            size: The side length of the game.
            seeds: Rectangle seeds on board as a dictionary of
                `(row, column): {"color": color, "area": area, "shape": shape}` items.
        
        Raises:
            TypeError: if type inputs are not respected.
            ValueError: If there are some seeds with the same color.
        """
        super().__init__(board_dims=(size, size))
        self.__set_seeds(seeds)
        self._model = PatchesModel(self.board_dims, self.__seeds)


    def __hash__(self) -> int:
        return hash((self._board_dims, self.__seeds))


    @property
    def size(self) -> int:
        """The side length of the game.

        Returns:
            The number of rows (or columns) on game's board.
        """
        return self.board_dims[0]


    @property
    def seeds(self) -> dict[tuple[int, int], dict[str, str | int | None]]:
        """
        The seeds of the game.
        
        Returns:
            All the information about the seeds as a dictionary of
                `(row, column): {"color": color, "area": area, "shape": shape}` items.
        """
        return {
            seed.square : {
                "color": seed.color_code,
                "shape": seed.shape,
                "area": seed.area
            } for seed in self.__seeds
        }


    def __set_seeds(self, seeds: dict[tuple[int, int], dict[str, str | int | None] | None]) -> None:

        if not isinstance(seeds, dict):
            msg = f"seeds must be a dictionary. Got {type(seeds).__name__} instead."
            raise TypeError(msg)

        if len(seeds) < 1:
            msg = "seeds cannot be empty!"
            raise ValueError(msg)

        seeds = {
            square: (
                {"color": None, "area": None, "shape": None} if seed is None
                else {
                    "color": seed["color"] if seed.get("color") not in (None, "") else None,
                    "area": seed.get("area"),
                    "shape": seed.get("shape")
                }
            ) for square, seed in seeds.items()
        }

        colors = [seed["color"] for seed in seeds.values() if seed["color"] is not None]
        if len(colors) != len(set(colors)):
            msg = "There must not be two or more seeds with the same color."
            raise ValueError(msg)

        if len(colors) < len(seeds):
            for seed in seeds.values():
                if seed["color"] is None:
                    random_color = self._generate_hex_code()
                    while random_color in colors:
                        random_color = self._generate_hex_code()
                    if seed is None:
                        seed = {"color": random_color}
                    else:
                        seed["color"] = random_color
                    colors.append(random_color)

        self.__seeds = [
            RectangleSeed(
                color=seed["color"],
                square=square,
                area=seed["area"],
                shape=seed["shape"]
            ) for square, seed in seeds.items()
        ]

        nx.set_node_attributes(self._board, "#FFFFFF", name="value")
        nx.set_node_attributes( # Adding a color for each square on the board
            self._board,
            name="value",
            values={
                tuple(i-1 for i in seed.square): seed.color
                for seed in self.__seeds
            }
        )

    @property
    def rectangles(self) -> list[dict[str, str | tuple[int, int]]] | None:
        """
        All rectangles that solves the Patches game.

        Returns:
            The solving rectangles as a list of dictionaries in the format
                `{"color_code": color_code, "top_left": (top, left), "dims": (height, width)}`.
        """
        if not self.is_solved:
            return None
        return sorted(
            [seed.rectangle.to_dict() for seed in self.__seeds],
            key=lambda x: x["top_left"]
        )

    def _set_solution(self, verbose:bool = False) -> None:

        u = self.model.u
        v = self.model.v
        I = self.model.I
        J = self.model.J
        for seed in self.__seeds:
            k = seed.color_code
            seed.rectangle = {
                "top": min(i for i in I if pyo.value(u[i,k]) > 0.5),
                "left": min(j for j in J if pyo.value(v[j,k]) > 0.5),
                "height": pyo.quicksum(round(pyo.value(u[i,k])) for i in I),
                "width": pyo.quicksum(round(pyo.value(v[j,k])) for j in J),
            }
        
        nx.set_node_attributes(
            self.board,
            name="value",
            values={
                (i-1, j-1): seed.color_code
                for seed in self.__seeds for (i,j) in seed.rectangle.squares
            }
        )

        if verbose:
            print("These are the rectagles that solves the game:")
            pprint(self.rectangles)


    def show(self) -> None:
        """Show Patches' board."""
        width = height = self.size * 0.5
        plt.figure(figsize=(width, height))
        nx.draw(
            self.board,
            pos={(i, j): (j, -i) for (i, j) in self.board.nodes()},
            node_size=1100,
            node_shape="s",
            node_color= list(nx.get_node_attributes(self.board, "value").values()),
            width=0,
            arrows=False,
            edgecolors="black",
            linewidths=1
        )
        plt.show()
