from math import sqrt
from matplotlib.colors import CSS4_COLORS
import re

from .rec_type import RecType


class TipSeed:

    def __init__(self, color:str, seed_square:tuple[int, int], rec_type:RecType, seed_area:int|None) -> None:
        self.color = color
        self.seed_square = seed_square
        self.rec_type = rec_type
        self.seed_area = seed_area


    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(\n\t"
            f"color={self.color},\n\t"
            f"seed_square={self.seed_square},\n\t"
            f"rec_type={type(self.rec_type).__name__}.{self.rec_type},\n\t"
            f"seed_area={self.seed_area}\n)"
        )


    def __str__(self) -> str:
        return (
            f"{type(self).__name__}("
            f"seed_square={self.seed_square}, "
            f"rec_type={type(self.rec_type).__name__}.{self.rec_type}, "
            f"seed_area={self.seed_area} "
            f"color={self.color})"
        )
    

    def __hash__(self) -> int:
        return hash((self._seed_square, self._rec_type, self._seed_area, self._color))
    

    def __len__(self) -> int:
        if self._seed_area:
            return self._seed_area
        else:
            return 0
    

    @staticmethod
    def __is_perfect_square(n:int) -> bool:
        return sqrt(n) % 1 == 0


    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, value:str="#FFFFFF") -> None:

        try:
            hex_code = CSS4_COLORS[value.strip().lower()]

        except KeyError:
            pattern = re.compile(r"^\#[0-9A-F]{6}$", re.IGNORECASE)

            if not isinstance(value, str) or re.fullmatch(pattern, value) is None:
                msg = f"The color must be a color name or a hex code like '#RRGGBB'. Got {value!r} instead."
                raise ValueError(msg)
            
            self._color = value

        else:
            self._color = hex_code


    @property
    def seed_square(self) -> tuple[int, int]:
        return self._seed_square

    @seed_square.setter
    def seed_square(self, value: tuple[int, int]) -> None:

        if not isinstance(value, tuple):
            msg = f"Seed square must be a tuple. Got a {type(value)} type instead."
            raise ValueError(msg)
        
        if len(value) != 2:
            msg = f"Seed square must be a pair (m,n). Got a tuple with length {len(value)}."
            raise ValueError(msg)
        
        if any(not isinstance(coord, int) or isinstance(coord, bool) or coord < 1 for coord in value):
            msg = f"Seed square coordinates must be positive integers. Got {value!r} instead."
            raise ValueError(msg)
        
        self._seed_square = value


    @property
    def rec_type(self) -> RecType:
        return self._rec_type

    @rec_type.setter
    def rec_type(self, value:RecType=RecType.ANY) -> None:

        if not isinstance(value, RecType):
            msg = f"The rectangle type must be a RecType class. Got a {type(value)} type instead."
            raise TypeError(msg)
        
        self._rec_type = value


    @property
    def seed_area(self) -> int | None:
        return self._seed_area

    @seed_area.setter
    def seed_area(self, value: int | None) -> None:
        # Allow None or a positive integer
        if value is not None and not isinstance(value, int):
            msg = f"The tip area must be an integer or None. Got {type(value)} instead."
            raise TypeError(msg)

        if value is not None:
            if value < 1:
                msg = f"The tip area must be a positive integer. Got {value!r} instead."
                raise ValueError(msg)

            if self.rec_type == RecType.SQUARE and not TipSeed.__is_perfect_square(value):
                msg = f"The tip area ({value!r}) is not a perfect square."
                raise ValueError(msg)

        self._seed_area = value
