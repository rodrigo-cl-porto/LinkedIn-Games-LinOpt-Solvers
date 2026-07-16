from linkedin_games import Patches
from linkedin_games.patches import SeedSquare, RectangleShape, Rectangle


def test_patches_16():

    seeds = tuple((
        SeedSquare(color_code="#846A0B", square=(1, 2), area=2),
        SeedSquare(color_code="#096B78", square=(1, 4), area=6),
        SeedSquare(color_code="#5A3DB1", square=(2, 6), area=2),
        SeedSquare(color_code="#0A7541", square=(3, 1), area=6),
        SeedSquare(color_code="#EF6C00", square=(3, 3), area=2, shape=RectangleShape.VERTICAL),
        SeedSquare(color_code="#E30102", square=(4, 4), area=4, shape=RectangleShape.SQUARE),
        SeedSquare(color_code="#097BB1", square=(4, 6), area=2),
        SeedSquare(color_code="#A01E4E", square=(5, 1), area=2),
        SeedSquare(color_code="#9B3C1C", square=(6, 3), area=6),
        SeedSquare(color_code="#503B36", square=(6, 5), area=4)
    ))

    patches = Patches((6, 6), seeds)
    patches.solve(solver="highs")

    solution =  tuple((
        Rectangle(left=1, top=1, width=2, height=1),
        Rectangle(left=3, top=1, width=3, height=2),
        Rectangle(left=6, top=1, width=1, height=2),
        Rectangle(left=1, top=2, width=2, height=3),
        Rectangle(left=3, top=3, width=1, height=2),
        Rectangle(left=4, top=3, width=2, height=2),
        Rectangle(left=6, top=3, width=1, height=2),
        Rectangle(left=1, top=5, width=1, height=2),
        Rectangle(left=2, top=5, width=3, height=2),
        Rectangle(left=5, top=5, width=2, height=2)
    ))

    assert patches.rectangles == solution


def test_patches_121():

    seeds = [
        SeedSquare(color_code="#846A0B", square=(1, 1), area=8),
        SeedSquare(color_code="#0A7541", square=(2, 5), area=8),
        SeedSquare(color_code="#5A3DB1", square=(3, 3)),
        SeedSquare(color_code="#EF6C00", square=(4, 4)),
        SeedSquare(color_code="#096B78", square=(5, 2), area=8),
        SeedSquare(color_code="#E30102", square=(6, 6), area=6, shape=RectangleShape.VERTICAL)
    ]

    patches = Patches((6, 6), seeds)
    patches.solve(solver="highs")

    solution = tuple((
        Rectangle(left=1, top=1, width=2, height=4),
        Rectangle(left=3, top=1, width=4, height=2),
        Rectangle(left=3, top=3, width=4, height=1),
        Rectangle(left=3, top=4, width=2, height=1),
        Rectangle(left=1, top=5, width=4, height=2),
        Rectangle(left=5, top=4, width=2, height=3),
    ))

    assert patches.rectangles == solution
