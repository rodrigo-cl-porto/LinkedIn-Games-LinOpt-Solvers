from linkedin_games import Patches

patches = Patches(
    size=6,
    seeds = {
        (1,1): {"color": "#846A0B", "area": 8},
        (2,5): {"color": "#0A7541", "area": 8},
        (3,3): {"color": "#5A3DB1", "area": None},
        (4,4): {"color": "#EF6C00", "shape": None},
        (5,2): {"color": "#096B78", "area": 8},
        (6,6): {"color": "#E30102", "area": 6, "shape": "vertical"},
    }
)
patches.solve().display()
