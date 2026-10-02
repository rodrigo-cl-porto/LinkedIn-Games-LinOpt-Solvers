from linkedin_games import Patches

patches = Patches(
    size=6,
    seeds = {
        (1,1): {"color": "yellow", "area": 8},
        (2,5): {"color": "green", "area": 8},
        (3,3): {"color": "purple", "area": None},
        (4,4): {"color": "orange", "shape": None},
        (5,2): {"color": "teal", "area": 8},
        (6,6): {"color": "red", "area": 6, "shape": "vertical"},
    }
)
patches.solve().display()
