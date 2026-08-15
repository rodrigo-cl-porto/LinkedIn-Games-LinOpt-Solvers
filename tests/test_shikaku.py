from linkedin_games.patches import Shikaku


def test_shikaku_2026_08_11_easy():
    shikaku = Shikaku(
        size=6,
        seeds={
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
    )
    shikaku.solve()
    rectangles = [
        {'dims': (1,2), 'top_left': (1,1)},
        {'dims': (2,3), 'top_left': (1,3)},
        {'dims': (2,1), 'top_left': (1,6)},
        {'dims': (3,2), 'top_left': (2,1)},
        {'dims': (2,1), 'top_left': (3,3)},
        {'dims': (2,2), 'top_left': (3,4)},
        {'dims': (2,1), 'top_left': (3,6)},
        {'dims': (2,1), 'top_left': (5,1)},
        {'dims': (2,3), 'top_left': (5,2)},
        {'dims': (2,2), 'top_left': (5,5)},
    ]
    assert shikaku.rectangles == rectangles


def test_shikaku_46():
    seeds = {
        (1,5): {"shape": "horizontal"},
        (2,3): {"shape": "horizontal"},
        (3,1): {"area": 8},
        (3,6): {"area": 10},
        (5,2): {"area": 3},
        (5,7): {"area": 14},
        (6,5): {"shape": "vertical"},
        (7,3): {"shape": "square"},
    }
    shikaku = Shikaku(8, seeds)
    shikaku.solve()
    rectangles = [
        {'dims': (8,1), 'top_left': (1,1)},
        {'dims': (1,7), 'top_left': (1,2)},
        {'dims': (1,5), 'top_left': (2,2)},
        {'dims': (7,2), 'top_left': (2,7)},
        {'dims': (2,5), 'top_left': (3,2)},
        {'dims': (1,3), 'top_left': (5,2)},
        {'dims': (4,2), 'top_left': (5,5)},
        {'dims': (3,3), 'top_left': (6,2)},
    ]
    assert shikaku.rectangles == rectangles


def test_shikaku_94():
    shikaku = Shikaku(
        size=8,
        seeds = {
            (1,1): {"area": 5},
            (1,8): {"area": 3},
            (2,2): {"area": 3},
            (2,7): {"area": 5},
            (3,4): None,
            (3,5): None,
            (4,2): {"area": 3},
            (4,7): {"area": 3},
            (5,2): {"area": 4},
            (5,7): {"area": 6},
            (6,4): None,
            (6,5): None,
            (7,2): {"area": 8},
            (7,7): {"area": 4},
            (8,1): {"area": 6},
            (8,8): {"area": 2},
        }
    )
    shikaku.solve()
    rectangles = [
        {'dims': (1,5), 'top_left': (1,1)},
        {'dims': (1,3), 'top_left': (1,6)},
        {'dims': (1,3), 'top_left': (2,1)},
        {'dims': (1,5), 'top_left': (2,4)},
        {'dims': (6,1), 'top_left': (3,1)},
        {'dims': (1,3), 'top_left': (3,2)},
        {'dims': (1,4), 'top_left': (3,5)},
        {'dims': (1,3), 'top_left': (4,2)},
        {'dims': (3,1), 'top_left': (4,5)},
        {'dims': (1,3), 'top_left': (4,6)},
        {'dims': (2,2), 'top_left': (5,2)},
        {'dims': (2,1), 'top_left': (5,4)},
        {'dims': (2,3), 'top_left': (5,6)},
        {'dims': (2,4), 'top_left': (7,2)},
        {'dims': (2,2), 'top_left': (7,6)},
        {'dims': (2,1), 'top_left': (7,8)},
    ]
    assert shikaku.rectangles == rectangles


def test_shikaku_121():
    shikaku = Shikaku(
        size=6,
        seeds = {
            (1,1): {"color": "#846A0B", "area": 8},
            (2,5): {"color": "#0A7541", "area": 8},
            (3,3): {"color": "#5A3DB1"},
            (4,4): {"color": "#EF6C00"},
            (5,2): {"color": "#096B78", "area": 8},
            (6,6): {"color": "#E30102", "area": 6, "shape": "vertical"},
        }
    )
    shikaku.solve()
    rectangles = [
        {'dims': (4,2), 'top_left': (1,1)},
        {'dims': (2,4), 'top_left': (1,3)},
        {'dims': (1,4), 'top_left': (3,3)},
        {'dims': (1,2), 'top_left': (4,3)},
        {'dims': (3,2), 'top_left': (4,5)},
        {'dims': (2,4), 'top_left': (5,1)},
    ]
    assert shikaku.rectangles == rectangles


def test_shikaku_141():
    seeds = {
        (1,7): {"shape": "square"},
        (3,3): {"area": 15},
        (6,6): {"area": 25},
        (8,2): {"shape": "vertical"},
    }
    shikaku = Shikaku(8, seeds)
    shikaku.solve()
    rectangles = [
        {'dims': (3,5), 'top_left': (1,1)},
        {'dims': (3,3), 'top_left': (1,6)},
        {'dims': (5,3), 'top_left': (4,1)},
        {'dims': (5,5), 'top_left': (4,4)},
    ]
    assert shikaku.rectangles == rectangles
