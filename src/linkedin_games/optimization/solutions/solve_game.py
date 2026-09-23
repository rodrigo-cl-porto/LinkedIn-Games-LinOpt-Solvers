from pyomo.environ import SolverFactory
from pyomo.opt import SolverStatus, TerminationCondition

from ...domain._game_grid import GameGrid
from ...domain._use_case import UseCase
from ..models._factory import OptimizationModelFactory


class SolveGame(UseCase):

    @staticmethod
    def execute(game: GameGrid, solver: str="highs", verbose: bool=False) -> str:
        opt_model = OptimizationModelFactory.create(game)
        result = SolverFactory(solver).solve(opt_model)
        is_solved = (
            result.Solver.status == SolverStatus.ok # Checks if solver is finished with normal termination and if...
            and (
                result.Solver.termination_condition == TerminationCondition.optimal # ended with an optimal solution...
                or result.Solver.termination_condition == TerminationCondition.feasible # or with a feasible one.
            )
        )

        if is_solved:
            print(f"{type(game).__name__} game solved successfully!")
            return result

        msg = "No feasible solution was found!"
        if verbose:
            msg += f"\n\n{result.Solver}"
        
        raise RuntimeError(msg)
