from typing import Any
from pprint import pprint

import matplotlib.pyplot as plt
import networkx as nx
import pyomo.environ as pyo

from ..._core._game_grid import GameGrid
from ..._mixin._color_generator_mixin import ColorGeneratorMixin
from ._model import ShikakuModel
from ._rectangle_seed import RectangleSeed


class Shikaku(ColorGeneratorMixin, GameGrid):
    """
    The Shikaku game.
    
    A game grid with some numbered squares that states the rectangles' areas
        to be built on the grid.

    Objective:
        Partition the grid into non-overlapping rectangular figures so that each geometric shape
        covers the numbered square with a area that matches the number on its numbered square.
    
    Rules:
        - Each numbered square (seed) must be covered by only one rectangle that has a area equal to its number;
        - A rectangle must cover only one seed;
    """
    def __init__(self, size:int, seeds: dict[tuple[int, int], int | dict[str, Any] | None]) -> None:
        """
        Args:
            size: The side length of the game.
            seeds: Rectangle seeds on grid as a dictionary of items as
                `(row, column) : area` or as `(row, column) : {"color": str, "area": int}`.
        
        Raises:
            TypeError: if type inputs are not respected.
            ValueError: If there are some seeds with the same color.
        """
        super().__init__(grid_dims=(size, size))
        self._set_seeds(seeds)
        self._set_model()


    def __hash__(self) -> int:
        return hash((self._grid_dims, self._seeds))


    @property
    def size(self) -> int:
        """
        The side length of the game.

        Returns:
            The number of rows (or columns) on game's grid.
        """
        return self.grid_dims[0]


    @property
    def seeds(self) -> list[dict[str, Any]]:
        """
        The seeds of the game.
        
        Returns:
            All the information about the seeds.
        """
        return [seed.to_dict() for seed in self._seeds]


    def _set_seeds(self, seeds: dict[tuple[int, int], int | dict[str, Any] | None]) -> None:
    
        if not isinstance(seeds, dict):
            msg = f"seeds must be a dictionary. Got {type(seeds).__name__} instead."
            raise TypeError(msg)

        if len(seeds) < 1:
            msg = "seeds cannot be empty!"
            raise ValueError(msg)

        rectangle_seeds = self._build_seeds(seeds)
        self._seeds = self.__set_seed_colors(rectangle_seeds)

        nx.set_node_attributes(self._grid, "#FFFFFF", name="value")
        nx.set_node_attributes( # Adding a color for each square on the grid
            self._grid,
            name="value",
            values={
                tuple(i-1 for i in seed.square): seed.color
                for seed in self._seeds
            }
        )


    @staticmethod
    def _build_seeds(seeds: dict[tuple[int, int], int | dict[str, Any] | None]) -> list[RectangleSeed]:
        return [
            RectangleSeed(
                square=square,
                color=seed.get("color") if isinstance(seed, dict) else "#FFFFFF",
                area=seed.get("area", 1) if isinstance(seed, dict) else seed if isinstance(seed, int) else 1,
            ) for square, seed in seeds.items()
        ]


    def __set_seed_colors(self, seeds: list[RectangleSeed]) -> list[RectangleSeed]:

        colors = [seed.color_code for seed in seeds if seed.color_code != "#FFFFFF"]
        if len(colors) != len(set(colors)):
            msg = "There must not be two or more seeds with the same color."
            raise ValueError(msg)

        if len(colors) < len(seeds):
            for seed in seeds:
                if seed.color_code == "#FFFFFF":
                    random_color = self._generate_hex_code()
                    while random_color in colors:
                        random_color = self._generate_hex_code()
                    seed.color = random_color
                    colors.append(random_color)
        
        return seeds


    def _set_model(self) -> None:
        self._model = ShikakuModel(self.grid_dims, self.seeds)


    @property
    def rectangles(self) -> list[dict[str, tuple[int, int]]] | None:
        """
        All rectangles that solves the Patches game.

        Returns:
            The solving rectangles as a list of dictionaries in the format
                `{"color_code": color_code, "top_left": (top, left), "dims": (height, width)}`.
        """
        if not self.is_solved:
            return None
        return sorted([seed.rectangle.to_dict() for seed in self._seeds], key=lambda rect: rect["top_left"])


    def _set_solution(self, verbose:bool = False) -> None:
        t = self.model.t
        l = self.model.l
        h = self.model.h
        w = self.model.w

        for seed in self._seeds:
            k = seed.color_code
            seed.rectangle = {
                "top": round(pyo.value(t[k])),
                "left": round(pyo.value(l[k])),
                "height": round(pyo.value(h[k])),
                "width": round(pyo.value(w[k]))
            }
        
        nx.set_node_attributes(
            self.grid,
            name="value",
            values={
                (i-1, j-1): seed.color_code
                for seed in self._seeds for (i,j) in seed.rectangle.squares
            }
        )

        if verbose:
            print("These are the rectagles that solves the game:")
            pprint(self.rectangles)


    def show(self) -> None:
        """Show Patches' grid."""
        width = height = self.size * 0.5
        plt.figure(figsize=(width, height))
        nx.draw(
            self.grid,
            pos={(i, j): (j, -i) for (i, j) in self.grid.nodes()},
            node_size=1100,
            node_shape="s",
            node_color= list(nx.get_node_attributes(self.grid, "value").values()),
            width=0,
            arrows=False,
            edgecolors="black",
            linewidths=1
        )
        plt.show()
