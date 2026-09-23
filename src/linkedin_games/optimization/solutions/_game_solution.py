from dataclasses import dataclass


@dataclass
class GameSolution:
    solution: dict[tuple[int, int], int]
