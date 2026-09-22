from pyomo.opt.results.solver import SolverStatus
from dataclasses import dataclass


@dataclass
class OptimizationResult:
    status: SolverStatus
    solution: dict[tuple[int, int], int]
