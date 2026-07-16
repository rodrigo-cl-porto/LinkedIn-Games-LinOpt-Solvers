<div align="center">
    <img src="./docs/images/linkedin-games-logo.svg" alt="LinkedIn Games' logo" height="150">
</div>

# 🐍 LinkedInGames 𖣯

LinkedInGames is a Python library that provides a set of tools to solve LinkedIn games ([Queens][linkedin-queens], [Tango][linkedin-tango], [Zip][linkedin-zip], [Mini Sudoku][linkedin-mini-sudoku] and [Patches][linkedin-patches] for now) by using linear optimization models. The library leverages popular Python libraries such as [Pyomo] for mathematical modeling and [NetworkX] for graph-based representations of game boards. 

This repository also contains a Jupyter Book that serves as a comprehensive guide to understanding and solving LinkedIn games using the LinkedInGames library. The book covers various topics, including the basics of optimization, the model structure of LinkedIn games, and step-by-step tutorials for solving them by using linear optimization.

[linkedin-queens]: https://www.linkedin.com/games/queens/
[linkedin-tango]: https://www.linkedin.com/games/tango/
[linkedin-zip]: https://www.linkedin.com/games/zip/
[linkedin-mini-sudoku]: https://www.linkedin.com/games/mini-sudoku/
[linkedin-patches]: https://www.linkedin.com/games/patches/
[Pyomo]: https://www.pyomo.org/
[NetworkX]: https://networkx.org/en/

# Installing

To install the LinkedInGames library, you can use `pip`:

```bash
pip install linkedin-games
```

Or run this command if you use `uv` as your project's environment manager (which I personally recommend):

```bash
uv add linkedin-games
```

# A Simple Example

In order to solve this Patches game:

<div align="center">
    <img src="./docs/images/patches-121.jpg" alt="Patches No. 121" height="150">
</div>

One can run this simple code snippet.

```python
from linkedin_games import Patches
from linkedin_games.patches import SeedSquare, RectangleShape


seeds = tuple((
    SeedSquare(color="#846A0B", square=(1, 2), area=2),
    SeedSquare(color="#846A0B", square=(1, 2), area=2),
    SeedSquare(color="#846A0B", square=(1, 2), area=2),
    SeedSquare(color="#846A0B", square=(1, 2), area=2),
))

patches = Patches((6, 6), seeds)
patches.solve(solver="highs") # Uses Highs solver
patches.show()
```

Which will return the following result:

<div align="center">
    <img src="" alt="" height="150px">
</div>

Which, by its turn, matches the official solution of this game:

<div align="center">
    <img src="./docs/images/patches-121-solution.jpg" alt="Solution of Patches No. 121" height="150">
</div>

# 📙 Jupyter Book

You can read the Jupyter Book to know more about the usage and behind-the-scenes implementation of this library on this 🔗[website].

[website]: https://rodrigo-cl-porto.github.io/Solving-LinkedIn-Games-by-Linear-Optimization/

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

[home]: https://rodrigo-cl-porto.github.io/Solving-LinkedIn-Games-by-Linear-Optimization/
[what-is-optimization]: https://rodrigo-cl-porto.github.io/Solving-LinkedIn-Games-by-Linear-Optimization/getting-started/what-is-optimization/
[linkedin-games-library]: https://rodrigo-cl-porto.github.io/Solving-LinkedIn-Games-by-Linear-Optimization/getting-started/linkedin-games-library/
[how-to-solve-queens]: https://rodrigo-cl-porto.github.io/Solving-LinkedIn-Games-by-Linear-Optimization/how-to-solve/queens/
[how-to-solve-tango]: https://rodrigo-cl-porto.github.io/Solving-LinkedIn-Games-by-Linear-Optimization/how-to-solve/tango/
[how-to-solve-zip]: https://rodrigo-cl-porto.github.io/Solving-LinkedIn-Games-by-Linear-Optimization/how-to-solve/zip/
[how-to-solve-mini-sudoku]: https://rodrigo-cl-porto.github.io/Solving-LinkedIn-Games-by-Linear-Optimization/how-to-solve/mini-sudoku/
[how-to-solve-patches]: https://rodrigo-cl-porto.github.io/Solving-LinkedIn-Games-by-Linear-Optimization/how-to-solve/patches/

# ❤️ Donate

If you find this library useful and would like to support its development, please consider making a [donation]. Your contributions will help me maintain my work, as well as fund future projects.

[donation]: https://github.com/sponsors/rodrigo-cl-porto
