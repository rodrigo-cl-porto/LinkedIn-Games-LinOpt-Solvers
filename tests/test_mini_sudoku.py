from linkedin_games.sudoku import Sudoku

# Solving Mini Sudoku No. 60

filled_squares = {
    (1,1): 1,
    (2,2): 2,
    (2,5): 3,
    (3,3): 3,
    (3,4): 6,
    (4,3): 5,
    (4,4): 4,
    (5,2): 4,
    (5,5): 5,
    (6,6): 6
}

mini_sudoku = Sudoku(6, (2,3), filled_squares)
mini_sudoku.solve(verbose=True)
mini_sudoku.show()
