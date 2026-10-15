from abc import ABC, abstractmethod
from typing import Any


class UseCase(ABC):
    @staticmethod
    @abstractmethod
    def execute(*args: Any, **kwargs: Any) -> None:
        ...
