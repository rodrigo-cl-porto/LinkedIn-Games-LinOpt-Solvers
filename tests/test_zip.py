from linkedin_games.zip import Zip

# Solving Zip No. 166

numbered_squares = {
    (1,1):  9,
    (1,2): 10,
    (1,3): 11,
    (2,1):  8,
    (2,4): 13,
    (3,1):  7,
    (3,4): 14,
    (3,5): 12,
    (4,2):  6,
    (4,3): 15,
    (4,6): 16,
    (5,3):  5,
    (5,6):  3,
    (6,4):  4,
    (6,5):  1,
    (6,6):  2
}

zip = Zip((6,6), numbered_squares)
zip.solve(solver="highs", verbose=True)
zip.show()
