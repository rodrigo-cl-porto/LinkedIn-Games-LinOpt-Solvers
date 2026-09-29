from enum import StrEnum


class PatchShape(StrEnum):
    """Valid rectangle shape required by a Patches seed."""
    ANY = "any"
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"
    SQUARE = "square"
