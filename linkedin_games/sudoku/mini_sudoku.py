from .sudoku import Sudoku


class MiniSudoku(Sudoku):

    def __init__(self, filled_squares: dict[tuple[int, int]: int]) -> None:
        super().__init__(6, (2,3), filled_squares)
