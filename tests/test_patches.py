from linkedin_games.patches import Patches, RectangleSeed, RectangleShape, Rectangle


def test_patches():

    # Solving Patches No. 16

    seeds = tuple((
        RectangleSeed( # Yellow
            color="#846A0B",
            square=(1, 2),
            shape=RectangleShape.ANY,
            area=2
        ),
        RectangleSeed( # Teal
            color="#096B78",
            square=(1, 4),
            shape=RectangleShape.ANY,
            area=6
        ),
        RectangleSeed( # Purple
            color="#5A3DB1",
            square=(2, 6),
            shape=RectangleShape.ANY,
            area=2
        ),
        RectangleSeed( # Green
            color="#0A7541",
            square=(3, 1),
            shape=RectangleShape.ANY,
            area=6
        ),
        RectangleSeed( # Orange
            color="#EF6C00",
            square=(3, 3),
            shape=RectangleShape.VERTICAL,
            area=2
        ),
        RectangleSeed( # Red
            color="#E30102",
            square=(4, 4),
            shape=RectangleShape.SQUARE,
            area=4
        ),
        RectangleSeed(
            color="#097BB1",
            square=(4, 6),
            shape=RectangleShape.ANY,
            area=2
        ), # Blue
        RectangleSeed( # Magenta
            color="#A01E4E",
            square=(5, 1),
            shape=RectangleShape.ANY,
            area=2
        ),
        RectangleSeed( # Brick
            color="#9B3C1C",
            square=(6, 3),
            shape=RectangleShape.ANY,
            area=6
        ),
        RectangleSeed( # Brown
            color="#503B36",
            square=(6, 5),
            shape=RectangleShape.ANY,
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
