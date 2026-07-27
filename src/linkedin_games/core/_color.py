import re
from typing import Self

from matplotlib.colors import CSS4_COLORS


class Color:
    """A class that provides color properties to a component."""

    __HEX_PATTERN: re.Pattern = re.compile(r"^\#[0-9A-F]{6}$")
    __COLOR_HEXES: dict[str, str] = CSS4_COLORS
    __COLOR_NAMES: dict[str, str] = {
        hex: name for name, hex in CSS4_COLORS.items()
    }

    def __init__(self, color:str="#FFFFFF") -> Self:
        self.color = color


    @staticmethod
    def __hex_to_rgb(hex: str) -> tuple[int, int, int]:
        """Convert '#RRGGBB' to an (R, G, B) tuple."""
        hex = hex.lstrip("#")
        return tuple(int(hex[i : i + 2], 16) for i in (0, 2, 4))


    @staticmethod
    def __get_closest_color_name(hex: str) -> str:
        """Find the closest color name from hex code by Euclidean distance."""
        if hex in Color.__COLOR_NAMES:
            return Color.__COLOR_NAMES[hex]

        target_rgb = Color.__hex_to_rgb(hex)
        closest_color = None
        min_distance = float("inf")

        for color, hex_val in Color.__COLOR_HEXES.items():
            color_rgb = Color.__hex_to_rgb(hex_val)
            distance_squared = sum(
                (t - c) ** 2 for t, c in zip(target_rgb, color_rgb)
            )

            if distance_squared < min_distance:
                min_distance = distance_squared
                closest_color = color

        return closest_color


    @staticmethod
    def __is_color_name(value:str) -> bool:
        value = value.replace(" ", "")
        return value in Color.__COLOR_HEXES


    @staticmethod
    def __is_hex_code(value:str) -> bool:
        return Color.__HEX_PATTERN.fullmatch(value) is not None


    @property
    def color(self) -> str:
        return self.__name

    @color.setter
    def color(self, value:str) -> None:

        if not isinstance(value, str):
            msg = (
                f"The color must be a string."
                f" Got a {type(value).__name__} instead."
            )
            raise ValueError(msg)
        
        color = " ".join(value.strip().lower().split())
        hex = " ".join(value.strip().upper().split())

        if Color.__is_hex_code(hex):
            self.__hex = hex
            self.__name = Color.__get_closest_color_name(hex)

        elif Color.__is_color_name(color):
            self.__name = color
            color = color.replace(" ", "")
            self.__hex = Color.__COLOR_HEXES[color]
        
        else:
            msg = (
                f"The color must be a valid color name or a hex code like '#RRGGBB'."
                f" Got {color!r} instead."
            )
            raise ValueError(msg)


    @property
    def hex(self) -> str:
        return self.__hex

    @hex.setter
    def hex(self, value:str) -> None:

        if not isinstance(value, str):
            msg = (
                f"The hex code must be a string."
                f" Got a {type(value).__name__} instead."
            )
            raise TypeError(msg)

        if not Color.__is_hex_code(value):
            msg = (
                f"The hex code must match to '#RRGGBB' pattern."
                f" Got {value!r} instead."
            )
            raise ValueError(msg)

        self.__hex = value
        self.__name = Color.__get_closest_color_name(value)


    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value:str) -> None:
        if not isinstance(value, str):
            msg = (
                "The color name must be a string."
                f" Got a {type(value).__name__} instead."
            )
            raise TypeError(msg)

        value = " ".join(value.strip().lower().split())
        if not Color.__is_color_name(value):
            msg = f"The name {value!r} is not a valid color."
            raise ValueError(msg)
        else:
            self.__hex = Color.__COLOR_HEXES[value.replace(" ", "")]
            self.__name = value
