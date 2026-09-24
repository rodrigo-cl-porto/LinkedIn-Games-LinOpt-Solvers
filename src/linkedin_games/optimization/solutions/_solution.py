from typing import Any


class GameSolution:

    def __init__(self) -> None:
        self._parts = {}

    def add(self, **kwargs: Any) -> None:
        self._parts.update(kwargs)

    def get(self, attr: str) -> Any:
        self._parts.get(attr)
