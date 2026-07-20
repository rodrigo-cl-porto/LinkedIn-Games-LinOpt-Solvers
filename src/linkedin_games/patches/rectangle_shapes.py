from enum import StrEnum


class RectangleShapes(StrEnum):
    """Rectangle shape required by a seed square."""

    ANY = "any"
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"
    SQUARE = "square"
