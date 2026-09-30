from abc import ABC, abstractmethod


class UseCase(ABC):
    @staticmethod
    @abstractmethod
    def execute(*args, **kwargs):
        ...
