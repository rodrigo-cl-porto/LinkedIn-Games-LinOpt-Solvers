from linkedin_games.tango import Tango


def test_tango():

    # Solving Tango No. 151

    # like (=) pairs, each element is ((i,j),(r,s))
    like_pairs = (
        ((2, 3), (2, 4)),
        ((2, 1), (3, 1)),
        ((2, 3), (3, 3)),
        ((2, 6), (3, 6)),
        ((4, 1), (4, 2)),
        ((6, 3), (6, 4)),
    )

    # opposite (X) pairs
    opp_pairs = (
        ((2, 4), (3, 4)),
        ((3, 1), (4, 1)),
        ((3, 3), (3, 4)),
        ((3, 6), (4, 6)),
        ((4, 5), (4, 6)),
    )

    # already filled squares: (i,j) -> kij
    filled_squares = {
        (1, 2): 1,
        (1, 5): 1,
        (5, 2): 0,
        (5, 5): 1,
    }

    tango = Tango((6,6), like_pairs, opp_pairs, filled_squares)
    tango.solve()

    solution = {
        (1, 1): 1,
        (1, 2): 1,
        (1, 3): 0,
        (1, 4): 0,
        (1, 5): 1,
        (1, 6): 0,
        (2, 1): 0,
        (2, 2): 0,
        (2, 3): 1,
        (2, 4): 1,
        (2, 5): 0,
        (2, 6): 1,
        (3, 1): 0,
        (3, 2): 1,
        (3, 3): 1,
        (3, 4): 0,
        (3, 5): 0,
        (3, 6): 1,
        (4, 1): 1,
        (4, 2): 1,
        (4, 3): 0,
        (4, 4): 0,
        (4, 5): 1,
        (4, 6): 0,
        (5, 1): 1,
        (5, 2): 0,
        (5, 3): 0,
        (5, 4): 1,
        (5, 5): 1,
        (5, 6): 0,
        (6, 1): 0,
        (6, 2): 0,
        (6, 3): 1,
        (6, 4): 1,
        (6, 5): 0,
        (6, 6): 1
    }

    assert tango.board_squares == solution
