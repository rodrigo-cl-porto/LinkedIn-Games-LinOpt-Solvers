from linkedin_games import Queens
from linkedin_games.queens import Region


def test_queens_307():

    # Solving Queens No. 307

    regions = {
        Region( # Purple
            color_code="#BBA3E1",
            squares={(1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (2,6), (2,7), (3,6), (3,7), (4,6), (4,7), (5,7), (6,7), (7,7)}
        ),
        Region( # Orange
            color_code="#FFC794", 
            squares={(2,1), (2,2), (2,3), (2,4), (3,1), (4,1), (4,2), (5,1), (5,2), (6,1), (6,2), (6,4), (6,5), (6,6), (7,1), (7,2), (7,3), (7,4), (7,5), (7,6)}
        ),
        Region( # Blue
            color_code="#94BEFF",
            squares={(2,5), (3,5)}
        ),
        Region( # Green
            color_code="#B3DF9E",
            squares={(3,2), (3,3)}
        ),
        Region( # Gray
            color_code="#E0E0E0",
            squares={(3,4), (4,3), (4,4), (4,5), (5,4)}
        ),
        Region( # Red
            color_code="#FF7B61",
            squares={(5,3), (6,3)}
        ),
        Region( # Yellow
            color_code="#E6F388",
            squares={(5,5), (5,6)}
        )
    }

    queens = Queens((7,7), regions)
    queens.solve()

    solution = [(1, 7), (2, 5), (3, 2), (4, 4), (5, 6), (6, 3), (7, 1)]

    assert queens.crowns == solution
