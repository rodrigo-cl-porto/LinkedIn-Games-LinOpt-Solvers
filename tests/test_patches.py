from linkedin_games import Patches
from linkedin_games.patches import SeedSquare, RectangleShape, Rectangle


def test_patches():

    # Solving Patches No. 16

    seeds = tuple((
        SeedSquare(
            color="#846A0B", # Olive
            square=(1, 2),
            area=2
        ),
        SeedSquare(
            color="#096B78", # Teal
            square=(1, 4),
            area=6
        ),
        SeedSquare(
            color="#5A3DB1", # Purple
            square=(2, 6),
            area=2
        ),
        SeedSquare(
            color="#0A7541", # Green
            square=(3, 1),
            area=6
        ),
        SeedSquare(
            color="#EF6C00", # Orange
            square=(3, 3),
            shape=RectangleShape.VERTICAL,
            area=2
        ),
        SeedSquare( 
            color="#E30102", # Red
            square=(4, 4),
            shape=RectangleShape.SQUARE,
            area=4
        ),
        SeedSquare(
            color="#097BB1", # Blue
            square=(4, 6),
            area=2
        ), 
        SeedSquare( 
            color="#A01E4E", # Magenta
            square=(5, 1),
            area=2
        ),
        SeedSquare( 
            color="#9B3C1C", # Brick
            square=(6, 3),
            area=6
        ),
        SeedSquare( 
            color="#503B36", # Brown
            square=(6, 5),
            area=4
        )
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
