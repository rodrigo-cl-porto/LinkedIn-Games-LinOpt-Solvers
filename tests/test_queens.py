from linkedin_games import Queens


def test_queens_307() -> None:
    regions = {
        "#BBA3E1": { # Purple
            (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (2,6),
            (2,7), (3,6), (3,7), (4,6), (4,7), (5,7), (6,7), (7,7)
        },
        "#FFC794": { # Orange
            (2,1), (2,2), (2,3), (2,4), (3,1), (4,1), (4,2),
            (5,1), (5,2), (6,1), (6,2), (6,4), (6,5), (6,6),
            (7,1), (7,2), (7,3), (7,4), (7,5), (7,6)
        },
        "#94BEFF": {(2,5), (3,5)}, # Blue
        "#B3DF9E": {(3,2), (3,3)}, # Green
        "#E0E0E0": {(3,4), (4,3), (4,4), (4,5), (5,4)}, # Gray
        "#FF7B61": {(5,3), (6,3)}, # Red
        "#E6F388": {(5,5), (5,6)} # Yellow
    }
    queens = Queens(7, regions)
    queens.solve()
    crowns = [(1,7), (2,5), (3,2), (4,4), (5,6), (6,3), (7,1)]
    assert queens.crowns == crowns


def test_queens_502() -> None:
    lightsteelblue = {(8,2), (9,2), (10,2), (10,3)}
    orange = {(8,1), (9,1), (10,1), (11,1), (11,2), (11,3)}
    turquoise = {(8,10), (9,9), (9,10), (10,8), (10,9), (10,10)}
    red = {(7,9), (8,8), (8,9), (9,6), (9,7), (9,8)}
    darkgray = {(6,8), (6,9), (6,10), (7,7), (7,8), (7,10)}
    gray = {(5,3), (6,1), (6,3), (6,4), (7,1), (7,2), (7,3), (8,3), (8,4)}
    pink = {(10,7)} | {(i,j) for i in range(6,12) for j in range(5,12) if i == 11 or j == 11}
    blue = {(1,10), (2,9), (2,10), (3,8), (3,9), (4,9), (5,7), (5,8), (5,9)}
    green = {(i,j) for i in range(1,6) for j in range(10,12)} - blue
    purple = {
        (6,2)} | {(i,j) for i in range(1,6) for j in range(1,8)
    } - {(2,7), (3,5), (3,6), (3,7), (4,6), (4,7), (5,3), (5,4), (5,5), (5,6), (5,7)}
    yellow = {
        (i,j) for i in range(1,12) for j in range(1,12)
    } - lightsteelblue - orange - turquoise - red - darkgray - gray - pink - blue - green - purple

    queens = Queens(
        size=11,
        regions={
            "#98CCD2": lightsteelblue,
            "#FFC794": orange,
            "#57ECE5": turquoise,
            "#FF7B61": red,
            "#B0A994": darkgray,
            "#DADADA": gray,
            "#DA96B5": pink,
            "#94BEFF": blue,
            "#B3DF9E": green,
            "#BBA3E1": purple,
            "#E6F388": yellow
        }
    )
    queens.solve()
    crowns = [(1,4), (2,9), (3,5), (4,10), (5,3), (6,11), (7,7), (8,2), (9,6), (10,8), (11,1)]
    assert queens.crowns == crowns


def test_queens_528() -> None:
    green = {(2,2), (2,3), (3,2), (4,2), (4,3)}
    orange = {(1,6), (2,5), (2,6), (2,7), (3,6)}
    blue = {(1,7), (1,8), (2,8), (2,9), (3,9)}
    beige = {(5,1), (5,2), (5,3), (6,2), (7,2)}
    red = {(5,5), (5,6), (5,7), (5,8), (6,6)}
    yellow = {(5,9), (5,10), (6,10), (7,10), (8,10)}
    gray = {(7,3), (8,2), (8,3), (9,2), (9,3)}
    cyan = {(8,5), (8,6), (9,6), (10,6), (10,7)}
    pink = {(7,9), (8,9), (9,9), (9,10), (10,10)}
    purple = {
        (i,j) for i in range(1,11) for j in range(1,11)
    } - green - orange - blue - beige - red - yellow - gray - cyan - pink

    queens = Queens(
        size=10,
        regions={
            "green": green,
            "orange": orange,
            "blue": blue,
            "beige": beige,
            "red": red,
            "yellow": yellow,
            "gray": gray,
            "cyan": cyan,
            "pink": pink,
            "purple": purple
        }
    )
    queens.solve()
    crowns = [(1,8), (2,5), (3,2), (4,4), (5,1), (6,6), (7,10), (8,3), (9,9), (10,7)]
    assert queens.crowns == crowns


def test_queens_827() -> None:
    beige = {(2,2), (3,2)}
    red = {(2,6), (2,7)}
    orange = {(i, 4) for i in range(1, 7)}
    blue = {(i,j) for i in range(1,5) for j in range(5,8)} - red
    green = {(i,8) for i in range(1,5)}
    yellow = {(5,7), (5,8)}
    gray = {(8,j) for j in range(1, 9)} | {(7,8)}
    purple = {(i,j) for i in range(1,8) for j in range(1,9)} - beige - red - orange - blue - green - yellow - gray

    queens = Queens(
        size=8,
        regions={
            "purple": purple,
            "gray": gray,
            "orange": orange,
            "blue": blue,
            "red": red,
            "green": green,
            "yellow": yellow,
            "beige": beige
        }
    )
    queens.solve()
    crowns = [(1,8), (2,6), (3,2), (4,5), (5,7), (6,4), (7,1), (8,3)]
    assert queens.crowns == crowns


def test_queens_829() -> None:
    red = {(i,j) for i in range(3, 6) for j in range(3, 6)} - {(4,4), (5,4)}
    purple = {(6,3), (7,3), (7,4), (7,5)}
    gray = {(7,6)} | {(i, 7) for i in range(3,8)}
    orange = {(1,5), (1,6), (1,7), (2,7)}
    green = {(i,j) for i in range(2,9) for j in range(2,9)} - red - purple - gray - orange
    pink = {(i,j) for i in range(1,6) for j in range(1,5)} - green - red
    beige = {(i,j) for i in range(6,10) for j in range(1,7)} - green - purple - gray
    blue = {(1,8), (1,9), (2,9), (3,9)}
    yellow = {(i,j) for i in range(4,10) for j in range(7,10)} - gray - green

    queens = Queens(
        size=9,
        regions={
            "red": red,
            "purple": purple,
            "gray": gray,
            "orange": orange,
            "green": green,
            "pink": pink,
            "beige": beige,
            "blue": blue,
            "yellow": yellow
        }
    )
    queens.solve()
    crowns = [(1,4), (2,7), (3,9), (4,2), (5,5), (6,3), (7,6), (8,1), (9,8)]
    assert queens.crowns == crowns
