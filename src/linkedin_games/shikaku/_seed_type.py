from typing import Required, TypedDict


class SeedType(TypedDict, total=False):
    color: str

class RectangleSeedType(SeedType, total=False):
    area: Required[int]
