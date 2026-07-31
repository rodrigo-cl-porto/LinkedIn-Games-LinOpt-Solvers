from linkedin_games import Patches


def test_patches_16():
    seeds = {
        (1,2): {"color": "#846A0B", "area": 2},
        (1,4): {"color": "#096B78", "area": 6},
        (2,6): {"color": "#5A3DB1", "area": 2},
        (3,1): {"color": "#0A7541", "area": 6},
        (3,3): {"color": "#EF6C00", "area": 2, "shape":"vertical"},
        (4,4): {"color": "#E30102", "area": 4, "shape":"square"},
        (4,6): {"color": "#097BB1", "area": 2},
        (5,1): {"color": "#A01E4E", "area": 2},
        (6,3): {"color": "#9B3C1C", "area": 6},
        (6,5): {"color": "#503B36", "area": 4},
    }
    patches = Patches((6,6), seeds)
    patches.solve()
    rectangles = [
        {"top_left": (1,1), "dims": (2,1)},
        {"top_left": (1,3), "dims": (3,2)},
        {"top_left": (1,6), "dims": (1,2)},
        {"top_left": (2,1), "dims": (2,3)},
        {"top_left": (3,3), "dims": (1,2)},
        {"top_left": (3,4), "dims": (2,2)},
        {"top_left": (3,6), "dims": (1,2)},
        {"top_left": (5,1), "dims": (1,2)},
        {"top_left": (5,2), "dims": (3,2)},
        {"top_left": (5,5), "dims": (2,2)},
    ]
    assert patches.rectangles == rectangles


def test_patches_121():
    seeds = {
        (1, 1): {"color": "#846A0B", "area": 8},
        (2, 5): {"color": "#0A7541", "area": 8},
        (3, 3): {"color": "#5A3DB1"},
        (4, 4): {"color": "#EF6C00"},
        (5, 2): {"color": "#096B78", "area": 8},
        (6, 6): {"color": "#E30102", "area": 6, "shape": "vertical"},
    }
    patches = Patches((6,6), seeds)
    patches.solve(solver="highs")
    rectangles = [
        {"top_left": (1,1), "dims": (2,4)},
        {"top_left": (1,3), "dims": (4,2)},
        {"top_left": (3,3), "dims": (4,1)},
        {"top_left": (4,3), "dims": (2,1)},
        {"top_left": (4,5), "dims": (2,3)},
        {"top_left": (5,1), "dims": (4,2)},
    ]
    assert patches.rectangles == rectangles
