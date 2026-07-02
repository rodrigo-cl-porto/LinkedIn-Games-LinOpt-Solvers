from linkedin_games.patches import Patches, TipSeed, RecType, Rectangle


def test_patches():

    # Solving Patches No. 16

    tip_seeds = tuple((
        TipSeed( # Yellow
            color="#846A0B",
            seed_square=(1, 2),
            rec_type=RecType.ANY,
            seed_area=2
        ),
        TipSeed( # Teal
            color="#096B78",
            seed_square=(1, 4),
            rec_type=RecType.ANY,
            seed_area=6
        ),
        TipSeed( # Purple
            color="#5A3DB1",
            seed_square=(2, 6),
            rec_type=RecType.ANY,
            seed_area=2
        ),
        TipSeed( # Green
            color="#0A7541",
            seed_square=(3, 1),
            rec_type=RecType.ANY,
            seed_area=6
        ),
        TipSeed( # Orange
            color="#EF6C00",
            seed_square=(3, 3),
            rec_type=RecType.VERTICAL,
            seed_area=2
        ),
        TipSeed( # Red
            color="#E30102",
            seed_square=(4, 4),
            rec_type=RecType.SQUARE,
            seed_area=4
        ),
        TipSeed(
            color="#097BB1",
            seed_square=(4, 6),
            rec_type=RecType.ANY,
            seed_area=2
        ), # Blue
        TipSeed( # Magenta
            color="#A01E4E",
            seed_square=(5, 1),
            rec_type=RecType.ANY,
            seed_area=2
        ),
        TipSeed( # Brick
            color="#9B3C1C",
            seed_square=(6, 3),
            rec_type=RecType.ANY,
            seed_area=6
        ),
        TipSeed( # Brown
            color="#503B36",
            seed_square=(6, 5),
            rec_type=RecType.ANY,
            seed_area=4
        )
    ))

    patches = Patches((6, 6), tip_seeds)
    patches.solve(solver="highs")

    solution =  tuple((
        Rectangle(
            color="#846A0B",
            seed_square=(1, 2),
            rec_type=RecType.ANY,
            seed_area=2,
            x=1,
            y=1,
            width=2,
            height=1
        ),
        Rectangle(
            color="#096B78",
            seed_square=(1, 4),
            rec_type=RecType.ANY,
            seed_area=6,
            x=3,
            y=1,
            width=3,
            height=2
        ),
        Rectangle(
            color="#5A3DB1",
            seed_square=(2, 6),
            rec_type=RecType.ANY,
            seed_area=2,
            x=6,
            y=1,
            width=1,
            height=2
        ),
        Rectangle(
            color="#0A7541",
            seed_square=(3, 1),
            rec_type=RecType.ANY,
            seed_area=6,
            x=1,
            y=2,
            width=2,
            height=3
        ),
        Rectangle(
            color="#EF6C00",
            seed_square=(3, 3),
            rec_type=RecType.VERTICAL,
            seed_area=2,
            x=3,
            y=3,
            width=1,
            height=2
        ),
        Rectangle(
            color="#E30102",
            seed_square=(4, 4),
            rec_type=RecType.SQUARE,
            seed_area=4,
            x=4,
            y=3,
            width=2,
            height=2
        ),
        Rectangle(
            color="#097BB1",
            seed_square=(4, 6),
            rec_type=RecType.ANY,
            seed_area=2,
            x=6,
            y=3,
            width=1,
            height=2
        ),
        Rectangle(
            color="#A01E4E",
            seed_square=(5, 1),
            rec_type=RecType.ANY,
            seed_area=2,
            x=1,
            y=5,
            width=1,
            height=2
        ),
        Rectangle(
            color="#9B3C1C",
            seed_square=(6, 3),
            rec_type=RecType.ANY,
            seed_area=6,
            x=2,
            y=5,
            width=3,
            height=2
        ),
        Rectangle(
            color="#503B36",
            seed_square=(6, 5),
            rec_type=RecType.ANY,
            seed_area=4,
            x=5,
            y=5,
            width=2,
            height=2
        )
    ))

    assert patches.rectangles == solution
