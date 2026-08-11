<div id="logo" align="center">
    <img src="./assets/logo.svg" alt="logo" width="30%">
</div>

<div id="project-metadata" align="center">
    <a href="https://pypi.org/project/linkedin-games/">
        <img src="https://img.shields.io/pypi/v/linkedin-games?logo=pypi&style=flat&color=blue&logoColor=gold" alt="PyPI - Package Version"/>
    </a>
    <a href="https://pypi.org/project/linkedin-games/">
        <img src="https://img.shields.io/pypi/pyversions/linkedin-games?logo=pypi&style=flat&color=blue&logoColor=gold" alt="PyPI - Python Version"/>
    </a>
    <a href="https://linkedin-games-linopt-solvers.readthedocs.io/">
        <img src="https://readthedocs.org/projects/linkedin-games-linopt-solvers/badge/?version=latest&style=flat" alt="Docs Status"/>
    </a>
    <a href="https://spdx.org/licenses/">
        <img src="https://img.shields.io/badge/license-MIT-9400d3.svg?style=flat&color=orange" alt="License - MIT"/>
    </a>
</div>

# 𖣯 LinkedIn Games Python Library

This is the documentation for LinkedIn Games Python package. This package provides a simple set of components to solve LinkedIn board games ([Queens][linkedin-queens], [Tango][linkedin-tango], [Zip][linkedin-zip], [Mini Sudoku][linkedin-mini-sudoku] and [Patches][linkedin-patches] for now) using Linear Optimization models.

[linkedin-queens]: https://www.linkedin.com/games/queens/
[linkedin-tango]: https://www.linkedin.com/games/tango/
[linkedin-zip]: https://www.linkedin.com/games/zip/
[linkedin-mini-sudoku]: https://www.linkedin.com/games/mini-sudoku/
[linkedin-patches]: https://www.linkedin.com/games/patches/

# Installing

To install the LinkedIn Games library, you can use the `pip` command:

```bash
pip install linkedin-games
```

Or run the command below if you use `uv` as your package manager:

```bash
uv add linkedin-games
```

# A Simple Example

In order to solve this Patches game:

<div align="center">
    <img src="./assets/patches-121.jpg" alt="Patches No. 121" width="40%">
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
patches = Patches(size=6, seeds=seeds)
patches.solve()
patches.show()
```

Which will return the following result:

<div align="center">
    <img src="./assets/patches-121-solved.png" alt="Patches No. 121 solved" width="40%">
</div>

Which, by its turn, matches the official solution of this game:

<div align="center">
    <img src="./assets/patches-121-solution.jpg" alt="Solution of Patches No. 121" width="40%">
</div>

# 📙 Jupyter Book

You can read more about the usage and implementation of this library on this [Jupyter Book].

[Jupyter Book]: https://rodrigo-cl-porto.github.io/LinkedIn-Games-LinOpt-Solvers/
