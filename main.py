from linkedin_games.tango import Tango

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
tango.solve(verbose=True)
tango.show()
