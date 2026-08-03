<div align="center">
    <img src="https://cdn.jsdelivr.net/gh/rodrigo-cl-porto/linkedin-games-solvers/docs/assets/logo.svg" alt="logo" width="40%">
</div>

# 🐍 Linear Optimization Solvers for LinkedIn Games 𖣯

This repository holds a Python package that provides a simple set of components to solve LinkedIn board games ([Queens][linkedin-queens], [Tango][linkedin-tango], [Zip][linkedin-zip], [Mini Sudoku][linkedin-mini-sudoku] and [Patches][linkedin-patches] for now) using Linear Optimization models. This library leverages popular Python libraries such as [Pyomo] for mathematical modeling and [NetworkX] for graph-based representations of game boards.

This repository also contains a Jupyter Book that teachs how this library implements Linear Optimization models to solve each game. The book introduces the basics of mathematical optimization, explain the components of the library and presents the line of reasoning behind the model's structure of each minigame.

[linkedin-queens]: https://www.linkedin.com/games/queens/
[linkedin-tango]: https://www.linkedin.com/games/tango/
[linkedin-zip]: https://www.linkedin.com/games/zip/
[linkedin-mini-sudoku]: https://www.linkedin.com/games/mini-sudoku/
[linkedin-patches]: https://www.linkedin.com/games/patches/
[Pyomo]: https://www.pyomo.org/
[NetworkX]: https://networkx.org/en/

# Installing

To install the LinkedIn Games library, you can use the `pip` command:

```bash
pip install linkedin-games
```

Or run the command below if you use `uv` as your package manager (which I personally recommend):

```bash
uv add linkedin-games
```

# A Simple Example

In order to solve this Patches game:

<div align="center">
    <img src="https://cdn.jsdelivr.net/gh/rodrigo-cl-porto/linkedin-games-solvers/docs/assets/patches-121.jpg" alt="Patches No. 121" width="40%">
</div>

One can run this simple code snippet.

```python
from linkedin_games import Patches


seeds = {
    (1,1): {"color": "yellow", "area"=8},
    (2,5): {"color": "green",  "area"=8},
    (3,3): {"color": "purple"},
    (4,4): {"color": "orange"},
    (5,2): {"color": "teal",   "area"=8},
    (6,6): {"color": "red",    "area"=6, "shape"="vertical"}
}
patches = Patches((6, 6), seeds)
patches.solve()
patches.show()
```

Which will return the following result:

<div align="center">
    <img src="https://cdn.jsdelivr.net/gh/rodrigo-cl-porto/linkedin-games-solvers/docs/assets/patches-121-solved.png" alt="Patches No. 121 solved" width="40%">
</div>

Which, by its turn, matches the official solution of this game:

<div align="center">
    <img src="https://cdn.jsdelivr.net/gh/rodrigo-cl-porto/linkedin-games-solvers/docs/assets/patches-121-solution.jpg" alt="Solution of Patches No. 121" width="40%">
</div>

# 📙 Jupyter Book

You can read more about the usage and implementation of this library on this [Jupyter Book].

[Jupyter Book]: https://rodrigo-cl-porto.github.io/linkedin-games-solvers/

## Table of Contents

- Solving Linkedin Games by Linear Optimization
    - [Home][home]
- Getting Started
    - [What is Optimization?][what-is-optimization]
    - [LinkedIn Games Library][linkedin-games-library]
- How to Solve
    - [Queens][how-to-solve-queens]
    - [Tango][how-to-solve-tango]
    - [Zip][how-to-solve-zip]
    - [Mini Sudoku][how-to-solve-mini-sudoku]
    - [Patches][how-to-solve-patches]

[home]: https://rodrigo-cl-porto.github.io/linkedin-games-solvers/
[what-is-optimization]: https://rodrigo-cl-porto.github.io/linkedin-games-solvers/getting-started/what-is-optimization/
[linkedin-games-library]: https://rodrigo-cl-porto.github.io/linkedin-games-solvers/getting-started/linkedin-games-library/
[how-to-solve-queens]: https://rodrigo-cl-porto.github.io/linkedin-games-solvers/how-to-solve/queens/
[how-to-solve-tango]: https://rodrigo-cl-porto.github.io/linkedin-games-solvers/how-to-solve/tango/
[how-to-solve-zip]: https://rodrigo-cl-porto.github.io/linkedin-games-solvers/how-to-solve/zip/
[how-to-solve-mini-sudoku]: https://rodrigo-cl-porto.github.io/linkedin-games-solvers/how-to-solve/mini-sudoku/
[how-to-solve-patches]: https://rodrigo-cl-porto.github.io/linkedin-games-solvers/how-to-solve/patches/

# ❤️ Donate

If you find this library useful and would like to support its development, please consider making a [donation]. Your contributions will help me maintain my work, as well as fund future projects.

[donation]: https://github.com/sponsors/rodrigo-cl-porto
