from typing import Any

from .._shared.domain.game_grid import GameGrid
from .._shared.optimization.solutions._solution import GameSolution
from .._shared.utils.color_generator import ColorGenerator
from ._seed import RectangleSeed
from ._solution import ShikakuSolution


class ShikakuGrid(GameGrid):

    def __init__(self, grid_dims: tuple[int, int], seeds: dict[tuple[int, int], dict[str, Any] | int | None]) -> None:
        super().__init__(grid_dims)
        self._set_seeds(seeds)
        self._solution: ShikakuSolution


    def __hash__(self) -> int:
        return hash((self._grid_dims, self._seeds))


    @property
    def seeds(self) -> dict[str, dict[str, Any]]:
        """
        The seeds of the game.

        Returns:
            All the information about the seeds.
        """
        return {color: seed.to_dict() for color, seed in self._seeds.items()}


    def _set_seeds(self, seeds: dict[tuple[int, int], Any]) -> None:

        if not isinstance(seeds, dict):
            msg = f"Seeds must be a dictionary. Got {type(seeds).__name__} instead."
            raise TypeError(msg)

        if len(seeds) < 1:
            msg = "seeds cannot be empty!"
            raise ValueError(msg)

        rectangle_seeds = self._build_seeds(seeds)
        rectangle_seeds = self.__set_seed_colors(rectangle_seeds)
        self._seeds = {seed.color_code: seed for seed in rectangle_seeds}


    @staticmethod
    def _build_seeds(seeds: dict[tuple[int, int], dict[str, Any] | int | None]) -> list[RectangleSeed]:
        return [
            RectangleSeed(
                square=square,
                color=seed.get("color") if isinstance(seed, dict) else "#FFFFFF",
                area=seed.get("area", 1) if isinstance(seed, dict) else seed if isinstance(seed, int) else 1,
            )
            for square, seed in seeds.items()
        ]


    def __set_seed_colors(self, seeds: list[RectangleSeed]) -> list[RectangleSeed]:

        colors = [seed.color_code for seed in seeds if seed.color_code != "#FFFFFF"]
        if len(colors) != len(set(colors)):
            msg = "There must not be two or more seeds with the same color."
            raise ValueError(msg)

        if len(colors) < len(seeds):
            for seed in seeds:
                if seed.color_code == "#FFFFFF":
                    random_color = ColorGenerator.generate_hex_code()
                    while random_color in colors:
                        random_color = ColorGenerator.generate_hex_code()
                    seed.color = random_color
                    colors.append(random_color)

        return seeds


    def set_solution(self, value: GameSolution) -> None:
    
        if not isinstance(value, ShikakuSolution):
            msg = f"Invalid input. Got {type(value).__name__} instead of GameSolution."
            raise TypeError(msg)

        for seed_color, rectangle in value.rectangles.items():
            seed = self._seeds[seed_color].to_dict()
            rectangle_area = rectangle.height * rectangle.width
            if seed["area"] is not None and rectangle_area != seed["area"]:
                msg = f"The patch's area ({rectangle_area}) doesn't attend to the required area ({seed['area']})."
                raise ValueError(msg)

        self._solution = value


    @property
    def grid_squares(self) -> dict[tuple[int, int], str | None]:
        if self._solution:
            return self._solution.grid_squares
        seed_squares = {seed.square: seed.color_code for seed in self._seeds.values()}
        return {(i, j): seed_squares.get((i, j)) for i in range(1, self._height + 1) for j in range(1, self._width + 1)}


    @property
    def rectangles(self) -> list[dict[str, tuple[int, int]] | None]:
        """
        All rectangles that solves the Patches game.

        Returns:
            The solving rectangles as a list of dictionaries in the format
                `{"color_code": color_code, "top_left": (top, left), "dims": (height, width)}`.
        """
        if self._solution:
            return sorted(
                [rectangle.to_dict() for rectangle in self._solution.rectangles.values()],
                key=lambda rectangle: rectangle["top_left"],
            )
        return []
