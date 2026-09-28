from typing import Any


class GameSolution:

    def __init__(self) -> None:
        self._parts: dict[str, Any] = {}


    def add(self, **kwargs: Any) -> None:
        self._parts.update(kwargs)


    def get(self, attr: str) -> Any:
        self._parts.get(attr)


    @property
    def grid_squares(self) -> dict[tuple[int, int], str | int | None]:
        return self.get("grid_squares")
