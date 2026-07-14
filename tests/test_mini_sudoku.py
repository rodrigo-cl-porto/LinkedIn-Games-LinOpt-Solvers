from linkedin_games import MiniSudoku


def test_mini_sudoku():

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

    mini_sudoku = MiniSudoku(filled_squares)
    mini_sudoku.solve()

    solution = {
        (1, 1): 1,
        (1, 2): 3,
        (1, 3): 4,
        (1, 4): 5,
        (1, 5): 6,
        (1, 6): 2,
        (2, 1): 5,
        (2, 2): 2,
        (2, 3): 6,
        (2, 4): 1,
        (2, 5): 3,
        (2, 6): 4,
        (3, 1): 4,
        (3, 2): 1,
        (3, 3): 3,
        (3, 4): 6,
        (3, 5): 2,
        (3, 6): 5,
        (4, 1): 2,
        (4, 2): 6,
        (4, 3): 5,
        (4, 4): 4,
        (4, 5): 1,
        (4, 6): 3,
        (5, 1): 6,
        (5, 2): 4,
        (5, 3): 2,
        (5, 4): 3,
        (5, 5): 5,
        (5, 6): 1,
        (6, 1): 3,
        (6, 2): 5,
        (6, 3): 1,
        (6, 4): 2,
        (6, 5): 4,
        (6, 6): 6
    }

    assert mini_sudoku.board_squares == solution
