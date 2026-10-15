---
title: LinkedIn Games Python Package
short_title: LinkedIn Games
date: 2026-10-08
---

The LinkedIn Games is a Python Package designed to solve the LinkedIn mini games by using Linear Optimization models and it will be the library to be used along this book.

# Dependencies

The Linkedin Games package has the following Python dependencies to model, solve and visualize the optimization problems:

[Pyomo](https://pyomo.org/)
: A powerful and flexible optimization modeling language that allows users to define optimization problems in a clear and concise way. Pyomo supports a wide range of optimization problem types, including linear, integer, and nonlinear programming, and can interface with various solvers.

[NetworkX](https://networkx.org/)
: A library for the creation, manipulation, and study of complex networks. It provides tools for working with graphs and networks, which can be useful for modeling and solving optimization problems that involve network structures.

[Matplotlib](https://matplotlib.org/)
: A plotting library for Python that provides a wide range of tools for creating static, animated, and interactive visualizations. It can be used to visualize optimization results, such as the feasible region, the objective function landscape, or the solution itself.

With this three libraries, it's able to model, solve and visualize the optimization problems we will encounter in this book. But...

:::{attention} Hold your horses! We need a solver first!
Pyomo is just a modeling language, it does not solve optimization problems by itself. In order to solve the optimization problems we will model with Pyomo, it's required an optimization solver.

[Highspy](https://pypi.org/project/highspy/)
: It provides an Python interface to the [Highs](https://www.highs.dev/), which is an open-source optimization solver that offers a good balance between performance and accessibility. Highs is free and open-source, making it an attractive option for users who want a powerful optimization tool without the need for a commercial license or subscription.

:::

# How to install

To install the LinkedIn Games package, you can use the traditional `pip` command:

```bash
pip install linkedin-games
```

Or run the command below if you use `uv` as your package manager:

```bash
uv add linkedin-games
```

# Abstract Base Classes

In order to understand how Pyomo work to build and solve the model before displaying the solution with NetworkX, it will be useful to check out the implementation of some Abstract Base Classes, which share methods and attributes with many other classes.

:::{seealso} Abstract Base Class
An abstract base class (ABC) is a class that cannot be instantiated and is designed to be subclassed. It can define **abstract methods** that must be implemented by its subclasses, providing a common interface for a group of related classes. It only makes sense to use an ABC if you have a set of classes that share some common behavior or attributes, and you want to enforce that certain methods are implemented in those subclasses by using the `@abstractmethod` decorator.

```python
from abc import ABC, abstractmethod


class Quadrilateral(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass


class Rectangle(Quadrilateral):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * (self.length + self.width)


class Square(Quadrilateral):
    def __init__(self, side_length):
        self.side_length = side_length

    def area(self):
        return self.side_length ** 2
    
    def perimeter(self):
        return 4 * self.side_length


class Diamond(Quadrilateral):
    def __init__(self, diagonal1, diagonal2):
        self.diagonal1 = diagonal1
        self.diagonal2 = diagonal2

    def area(self):
        return (self.diagonal1 * self.diagonal2) / 2

    def perimeter(self):
        side_length = ((self.diagonal1 / 2) ** 2 + (self.diagonal2 / 2) ** 2) ** 0.5
        return 4 * side_length


class Trapeze(Quadrilateral):
    def __init__(self, base1, base2, height):
        self.base1 = base1
        self.base2 = base2
        self.height = height

    def area(self):
        return (self.base1 + self.base2) * self.height / 2

    def perimeter(self):
        # For a trapeze, we need the lengths of the non-parallel sides.
        # Assuming it's an isosceles trapezoid for simplicity.
        side_length = ((self.base2 - self.base1) / 2) ** 2 + self.height ** 2
        side_length = side_length ** 0.5
        return self.base1 + self.base2 + 2 * side_length
```
:::

## `GameModeler`

The `GameModeler` is a [builder pattern](https://refactoring.guru/design-patterns/builder) that sets the Pyomo `ConcreteModel`'s components of a game. This base class creates the basic components shared with all games, such as:

Board dimension parameters `m` and `n`
: The total number of rows and columns on game's board.

Range sets `I` and `J`
: The ranges of rows and columns, respectively.

Set `S`
: The set of all squares on game board, which is a cartesian product between ranges `I` and `J`.

:::{literalinclude} ../../src/linkedin_games/_shared/optimization/modeler/opt_modeler.py
:caption: The game modeler's base class
:label: game-modeler
:lang: python
:linenos:
:::

:::{note} Feasibility Problem
When a optimization problem actually doesn't have any function to maximize or minimize, it is called a **feasibility** problem, since the objective is not to find an optimal solution, but a **feasible** one that satisfies all model's constraints. To formulate a feasibility problem, the objective function is defined as to maximize (or minimize, it doesn't matter in this case) an arbitrary constant $C$ (personally, I prefer to set $C=0$ to indicate the objective function is turned off).

```{math}
:enumerated: false
\text{Max} \quad C \iff \text{Min} \quad C
```

As you will see further, all the LinkedIn mini games are formulated as feasibility problems, since the goal is to find a solution that satisfies all the rules of the game, rather than optimizing a specific objective function. This is implemented in the `GameModeler` class, which sets the objective function to maximize zero.

```{literalinclude} ../../src/linkedin_games/_shared/optimization/modeler/opt_modeler.py
:caption: The game modeler's objective function sets the game's model as a feasibility problem.
:label: feasibility-problem
:lang: python
:linenos:
:start-at: def _set_objective_function
:end-at: self._model.obj
```

:::

## `GameRenderer`

The `GameRenderer` is plays the role to display the game's board by using the NetworkX, to build the graph structure, and Matplotlib, to plot the board as a chart.

:::{literalinclude} ../../src/linkedin_games/_shared/visualization/renderer/renderer.py
:caption: The game renderer's base class
:label: game-renderer
:lang: python
:linenos:
:::

:::{seealso} PyPI Page
You can find the LinkedIn Games Python Package on [PyPI](https://pypi.org/project/linkedin-games/), where you can check the latest version, release history, and additional information about the package.
:::