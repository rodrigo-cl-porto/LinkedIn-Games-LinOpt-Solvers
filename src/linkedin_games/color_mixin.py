from __future__ import annotations
from matplotlib.colors import CSS4_COLORS
import re


class ColorMixin:
    """Mixin that provides a color value and its closest CSS4 color name."""

    __HEX_PATTERN: re.Pattern = re.compile(r"^\#[0-9A-F]{6}$", re.IGNORECASE)
    __DEFAULT_COLOR: str      = "white"
    __DEFAULT_COLOR_CODE: str = "#FFFFFF"


    def __init__(self, color:str | None = None, color_code:str | None = None):

        if color is not None and color_code is not None:
            msg = "Inform only the color name OR its hex code, not both."
            raise ValueError(msg)
        
        if color is None and color_code is None:
            self._color = ColorMixin.__DEFAULT_COLOR
            self._color_code = ColorMixin.__DEFAULT_COLOR_CODE
        
        if color_code is None:
            self.color = color

        if color is None:
            self.color_code = color_code


    @staticmethod
    def __hex_to_rgb(hex_code: str) -> tuple[int, int, int]:
        """Converts '#RRGGBB' to an (R, G, B) tuple."""
        hex_code = hex_code.lstrip("#")
        return tuple(int(hex_code[i : i + 2], 16) for i in (0, 2, 4))


    @staticmethod
    def __get_closest_color(hex_code: str) -> str:
        """Finds the closest color name by Euclidean distance."""
        target_rgb = ColorMixin.__hex_to_rgb(hex_code)
        closest_name = None
        min_distance = float("inf")

        for name, hex_val in CSS4_COLORS.items():
            color_rgb = ColorMixin.__hex_to_rgb(hex_val)
            distance_squared = sum((t - c) ** 2 for t, c in zip(target_rgb, color_rgb))

            if distance_squared < min_distance:
                min_distance = distance_squared
                closest_name = name

        return closest_name


    @property
    def color_code(self) -> str:
        return self._color_code

    @color_code.setter
    def color_code(self, value:str) -> None:

        if not isinstance(value, str):
            msg = f"The color must be a hex code. Got {value!r} instead."
            raise ValueError(msg)

        value = value.strip()

        if ColorMixin.__HEX_PATTERN.fullmatch(value) is None:
            msg = f"The color must be a hex code like '#RRGGBB'. Got {value!r} instead."
            raise ValueError(msg)

        self._color_code = value
        self._color = ColorMixin.__get_closest_color(value)


    @property
    def color(self) -> str:
        """Closest CSS4 color name for the current hex color."""
        return self._color

    @color.setter
    def color(self, value:str) -> None:

        if not isinstance(value, str):
            msg = f"The color name must be a string. Got {value!r} instead."
            raise TypeError(msg)

        value = value.strip().lower()

        try:
            self._color_code = CSS4_COLORS[value]

        except KeyError: # The color name is not a valid one
            msg = f"The color is not a valid name. Got {value!r} instead."
            raise ValueError(msg)
        
        else:
            self._color = value
