from typing import ClassVar
import re
from matplotlib.colors import CSS4_COLORS


class Color:
    """Class to provide color properties to a component."""

    __HEX_PATTERN: re.Pattern = re.compile(r"\#[0-9A-F]{6}")
    __COLOR_HEXES = CSS4_COLORS
    __COLOR_NAMES: ClassVar = {hex_code: name for name, hex_code in CSS4_COLORS.items()}

    def __init__(self, color: str|None="#FFFFFF") -> object:
        """
        Args:
            color: Color name or its hex code as a "#RRGGBB" string.
        """
        self.color = color


    @staticmethod
    def __hex_code_to_rgb(hex_code: str) -> tuple[int,...]:
        """Convert '#RRGGBB' to an (R, G, B) tuple."""
        hex_code = hex_code.lstrip("#")
        return tuple(int(hex_code[i : i + 2], 16) for i in (0, 2, 4))


    @staticmethod
    def __get_closest_color_name(hex_code: str) -> str:
        """Find the closest color name from hex code by Euclidean distance."""
        if hex_code in Color.__COLOR_NAMES:
            return Color.__COLOR_NAMES[hex_code]

        target_rgb = Color.__hex_code_to_rgb(hex_code)
        closest_color = "#FFFFFF"
        min_distance = float("inf")

        for color, hex_val in Color.__COLOR_HEXES.items():
            color_rgb = Color.__hex_code_to_rgb(str(hex_val))
            distance_squared = sum(
                (t - c) ** 2 for t, c in zip(target_rgb, color_rgb, strict=True)
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
    def color(self, value: str|None) -> None:

        if value is None:
            self.__name = "white"
            self.__hex_code = "#FFFFFF"
            return

        if not isinstance(value, str):
            msg = f"The color must be a string. Got a {type(value).__name__} instead."
            raise TypeError(msg)
        
        color = " ".join(value.strip().lower().split())
        hex_code = " ".join(value.strip().upper().split())

        if Color.__is_hex_code(hex_code):
            self.__hex_code = hex_code
            self.__name = Color.__get_closest_color_name(hex_code)

        elif Color.__is_color_name(color):
            self.__name = color
            color = color.replace(" ", "")
            self.__hex_code = Color.__COLOR_HEXES[color]
        
        else:
            msg = f"The color must be a valid color name or a hex code like '#RRGGBB'. Got {color!r} instead."
            raise ValueError(msg)


    @property
    def hex_code(self) -> str:
        return str(self.__hex_code)

    @hex_code.setter
    def hex_code(self, value:str | None) -> None:

        if not isinstance(value, str):
            msg = f"The hex code must be a string. Got a {type(value).__name__} instead."
            raise TypeError(msg)

        if not Color.__is_hex_code(value):
            msg = f"The hex code must match to '#RRGGBB' pattern. Got {value!r} instead."
            raise ValueError(msg)

        self.__hex_code = str(value)
        self.__name = Color.__get_closest_color_name(value)


    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str| None) -> None:

        if not isinstance(value, str):
            msg = f"The color name must be a string. Got a {type(value).__name__} instead."
            raise TypeError(msg)

        value = " ".join(value.strip().lower().split())
        if not Color.__is_color_name(value):
            msg = f"The name {value!r} is not a valid color."
            raise ValueError(msg)
        
        self.__hex_code = Color.__COLOR_HEXES[value.replace(" ", "")]
        self.__name = value
