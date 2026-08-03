<div align="center">
    <img src="https://cdn.jsdelivr.net/gh/rodrigo-cl-porto/LinkedIn-Games-LinOpt-Solvers/docs/assets/logo.svg" alt="logo" width="20%">
</div>

<div align="center">
    
[![PyPI - Package Version](https://img.shields.io/pypi/v/linkedin-games?logo=pypi&style=flat&color=blue&logoColor=gold)](https://pypi.org/project/linkedin-games/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/linkedin-games?logo=pypi&style=flat&color=blue&logoColor=gold)](https://pypi.org/project/linkedin-games/)
[![PyPI - Installs](https://img.shields.io/pypi/dm/linkedin-games?logo=pypi&style=flat&color=blue&logoColor=gold)](https://pypi.org/project/linkedin-games/)
[![Documentation Status](https://readthedocs.org/projects/linkedin-games-linopt-solvers/badge/?version=latest&style=flat)](https://linkedin-games-linopt-solvers.readthedocs.io/)
[![License - MIT](https://img.shields.io/badge/license-MIT-9400d3.svg?style=flat&color=orange)](https://spdx.org/licenses/)

</div>

<div align="center">

[![Last Commit](https://img.shields.io/github/last-commit/rodrigo-cl-porto/LinkedIn-Games-LinOpt-Solvers/main?style=social&logo=github)](https://github.com/rodrigo-cl-porto/LinkedIn-Games-LinOpt-Solvers)
[![GitHub Stars](https://img.shields.io/github/stars/rodrigo-cl-porto/LinkedIn-Games-LinOpt-Solvers)](https://github.com/rodrigo-cl-porto/LinkedIn-Games-LinOpt-Solvers)
[![GitHub Sponsors](https://img.shields.io/github/sponsors/rodrigo-cl-porto?logo=GitHub%20Sponsors&style=social)](https://github.com/sponsors/rodrigo-cl-porto)

</div>

<div align="center">

[![package manager - uv](https://img.shields.io/endpoint?style=flat&url=https%3A%2F%2Fraw.githubusercontent.com%2FOnyx-Nostalgia%2Fuv%2Frefs%2Fheads%2Ffix%2Flogo-badge%2Fassets%2Fbadge%2Fv0.json)](https://github.com/astral-sh/uv)
[![linting - Ruff](https://img.shields.io/endpoint?style=flat&url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![testing - pytest](https://img.shields.io/badge/py-test-blue?logo=pytest&style=flat)](https://github.com/pytest-dev/pytest)
[![task runner - Poe The Poet](https://img.shields.io/badge/poe-the_poet-white)](https://github.com/nat-n/poethepoet)

</div>

<div align="center">

[![book - Jupyter Book](https://raw.githubusercontent.com/jupyter-book/jupyter-book/next/docs/media/images/badge.svg)](https://jupyterbook.org)
[![documentation - Zensical](https://img.shields.io/badge/docs-zensical-orange?logo=zensical&style=flat)](https://github.com/zensical/zensical)

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
    <img src="https://cdn.jsdelivr.net/gh/rodrigo-cl-porto/LinkedIn-Games-LinOpt-Solvers/docs/assets/patches-121.jpg" alt="Patches No. 121" width="40%">
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
    <img src="https://cdn.jsdelivr.net/gh/rodrigo-cl-porto/LinkedIn-Games-LinOpt-Solvers/docs/assets/patches-121-solved.png" alt="Patches No. 121 solved" width="40%">
</div>

Which, by its turn, matches the official solution of this game:

<div align="center">
    <img src="https://cdn.jsdelivr.net/gh/rodrigo-cl-porto/LinkedIn-Games-LinOpt-Solvers/docs/assets/patches-121-solution.jpg" alt="Solution of Patches No. 121" width="40%">
</div>

# 📙 Jupyter Book

You can read more about the usage and implementation of this library on this [Jupyter Book].

[Jupyter Book]: https://rodrigo-cl-porto.github.io/LinkedIn-Games-LinOpt-Solvers/

## Table of Contents

- Solving LinkedIn Games by Linear Optimization
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

[home]: https://rodrigo-cl-porto.github.io/LinkedIn-Games-LinOpt-Solvers/
[what-is-optimization]: https://rodrigo-cl-porto.github.io/LinkedIn-Games-LinOpt-Solvers/getting-started/what-is-optimization/
[linkedin-games-library]: https://rodrigo-cl-porto.github.io/LinkedIn-Games-LinOpt-Solvers/getting-started/linkedin-games-library/
[how-to-solve-queens]: https://rodrigo-cl-porto.github.io/LinkedIn-Games-LinOpt-Solvers/how-to-solve/queens/
[how-to-solve-tango]: https://rodrigo-cl-porto.github.io/LinkedIn-Games-LinOpt-Solvers/how-to-solve/tango/
[how-to-solve-zip]: https://rodrigo-cl-porto.github.io/LinkedIn-Games-LinOpt-Solvers/how-to-solve/zip/
[how-to-solve-mini-sudoku]: https://rodrigo-cl-porto.github.io/LinkedIn-Games-LinOpt-Solvers/how-to-solve/mini-sudoku/
[how-to-solve-patches]: https://rodrigo-cl-porto.github.io/LinkedIn-Games-LinOpt-Solvers/how-to-solve/patches/

# ❤️ Donate

If you find this library useful and would like to support its development, please consider making a [donation]. Your contributions will help me maintain my work, as well as fund future projects.

[donation]: https://github.com/sponsors/rodrigo-cl-porto
