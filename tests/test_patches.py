from linkedin_games import Patches
from linkedin_games.patches import SeedSquare, Rectangle


def test_patches_16():

    seeds = tuple((
        SeedSquare(color="#846A0B", square=(1, 2), area=2),
        SeedSquare(color="#096B78", square=(1, 4), area=6),
        SeedSquare(color="#5A3DB1", square=(2, 6), area=2),
        SeedSquare(color="#0A7541", square=(3, 1), area=6),
        SeedSquare(color="#EF6C00", square=(3, 3), area=2, shape="vertical"),
        SeedSquare(color="#E30102", square=(4, 4), area=4, shape="square"),
        SeedSquare(color="#097BB1", square=(4, 6), area=2),
        SeedSquare(color="#A01E4E", square=(5, 1), area=2),
        SeedSquare(color="#9B3C1C", square=(6, 3), area=6),
        SeedSquare(color="#503B36", square=(6, 5), area=4)
    ))

    patches = Patches((6, 6), seeds)
    patches.solve()

    solution =  tuple((
        Rectangle(color="#846A0B", top_left_square=(1,1), dims=(2,1)),
        Rectangle(color="#096B78", top_left_square=(1,3), dims=(3,2)),
        Rectangle(color="#5A3DB1", top_left_square=(1,6), dims=(1,2)),
        Rectangle(color="#0A7541", top_left_square=(2,1), dims=(2,3)),
        Rectangle(color="#EF6C00", top_left_square=(3,3), dims=(1,2)),
        Rectangle(color="#E30102", top_left_square=(3,4), dims=(2,2)),
        Rectangle(color="#097BB1", top_left_square=(3,6), dims=(1,2)),
        Rectangle(color="#A01E4E", top_left_square=(5,1), dims=(1,2)),
        Rectangle(color="#9B3C1C", top_left_square=(5,2), dims=(3,2)),
        Rectangle(color="#503B36", top_left_square=(5,5), dims=(2,2))
    ))

    assert patches.rectangles == solution


def test_patches_121():

    seeds = [
        SeedSquare(color="#846A0B", square=(1, 1), area=8),
        SeedSquare(color="#0A7541", square=(2, 5), area=8),
        SeedSquare(color="#5A3DB1", square=(3, 3)),
        SeedSquare(color="#EF6C00", square=(4, 4)),
        SeedSquare(color="#096B78", square=(5, 2), area=8),
        SeedSquare(color="#E30102", square=(6, 6), area=6, shape="vertical")
    ]

    patches = Patches((6, 6), seeds)
    patches.solve(solver="highs")

    solution = tuple((
        Rectangle(color="#846A0B", top_left_square=(1,1), dims=(2,4)),
        Rectangle(color="#0A7541", top_left_square=(1,3), dims=(4,2)),
        Rectangle(color="#5A3DB1", top_left_square=(3,3), dims=(4,1)),
        Rectangle(color="#EF6C00", top_left_square=(4,3), dims=(2,1)),
        Rectangle(color="#096B78", top_left_square=(5,1), dims=(4,2)),
        Rectangle(color="#E30102", top_left_square=(4,5), dims=(2,3))
    ))

    assert patches.rectangles == solution
