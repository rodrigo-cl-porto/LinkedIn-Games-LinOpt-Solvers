from linkedin_games.patches import Patches, TipSeed, RecType

# Solving Patches No. 16

tip_seeds = (
    TipSeed( # Yellow
        color="#846A0B",
        seed_square=(1, 2),
        rect_type=RecType.ANY,
        seed_area=2
    ),
    TipSeed( # Teal
        color="#096B78",
        seed_square=(1, 4),
        rect_type=RecType.ANY,
        seed_area=6
    ),
    TipSeed( # Purple
        color="#5A3DB1",
        seed_square=(2, 6),
        rect_type=RecType.ANY,
        seed_area=2
    ),
    TipSeed( # Green
        color="#0A7541",
        seed_square=(3, 1),
        rect_type=RecType.ANY,
        seed_area=6
    ),
    TipSeed( # Orange
        color="#EF6C00",
        seed_square=(3, 3),
        rect_type=RecType.VERTICAL,
        seed_area=2
    ),
    TipSeed( # Red
        color="#E30102",
        seed_square=(4, 4),
        rect_type=RecType.SQUARE,
        seed_area=4
    ),
    TipSeed(
        color="#097BB1",
        seed_square=(4, 6),
        rect_type=RecType.ANY,
        seed_area=2
    ), # Blue
    TipSeed( # Magenta
        color="#A01E4E",
        seed_square=(5, 1),
        rect_type=RecType.ANY,
        seed_area=2
    ),
    TipSeed( # Brick
        color="#9B3C1C",
        seed_square=(6, 3),
        rect_type=RecType.ANY,
        seed_area=6
    ),
    TipSeed( # Brown
        color="#503B36",
        seed_square=(6, 5),
        rect_type=RecType.ANY,
        seed_area=4
    )
)

patches = Patches((6, 6), tip_seeds)
patches.solve(solver="highs", verbose=True)
patches.show()
