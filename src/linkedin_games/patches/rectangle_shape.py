from enum import StrEnum


class RectangleShape(StrEnum):
    """Rectangle shape required by a seed square."""

    ANY = "ANY"
    VERTICAL = "VERTICAL"
    HORIZONTAL = "HORIZONTAL"
    SQUARE = "SQUARE"
