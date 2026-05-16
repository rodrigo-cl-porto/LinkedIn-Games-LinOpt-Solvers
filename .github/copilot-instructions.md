# Copilot instructions for this repository

Purpose
- Help AI assistants understand how to build, run, and explore this repo quickly.

1) Build, test, and lint commands
- Make targets (root Makefile):
  - make setup  — creates venv via `uv` and syncs deps (uses Python 3.13 per Makefile).
  - make start  — starts the Jupyter Book dev server (runs `jupyter-book start` in book/).
  - make build  — builds the Jupyter Book HTML (runs `jupyter-book build --html` in book/).
  - make deploy — prepares the book for GitHub Pages (runs `jupyter-book init --gh-pages`).
  - make clean  — removes .venv
- Direct commands (Windows/explicit):
  - cd book && jupyter-book start
  - cd book && jupyter-book build --html
- Notes on testing/linting: no dedicated test suite or linter configuration detected. There are example scripts under linkedin-games/ that can be executed directly (see below).

2) How to run a single example (quick)
- Execute the example script directly (Windows):
  - python linkedin-games\queens\queens.py
  - python linkedin-games\zip\zip.py
  - python linkedin-games\tango\tango.py
- Alternatively install the project and run notebooks/book: `pip install -e .` then use the book in `book/`.

3) High-level architecture (big picture)
- Docs: a Jupyter Book lives in the book/ directory and contains the user-facing examples and narrative. Building/serving is done by jupyter-book.
- Code: the core examples live in the `linkedin-games/` directory. Each subdirectory is a self-contained puzzle implementation (examples: zip, tango, queens, mini-sudoku, patches).
- Module pattern: each puzzle module typically defines a class inheriting from pyomo.environ.ConcreteModel with:
  - __init__ constructing sets/params/vars/constraints/objective
  - solve(self) calling a solver via pyo.SolverFactory (gurobi or highs)
  - show(self) visualizing the solution with networkx/matplotlib
- Example scripts include `if __name__ == "__main__":` blocks with concrete instance data so files can be executed as standalone demonstrations.

4) Key conventions and repo-specific notes
- Dependency/solvers:
  - Requires Pyomo and either gurobipy (license required) or highs (open-source) depending on the example. Check each module's solve() for which solver is used.
  - The pyproject.toml lists runtime deps: gurobipy, highspy, matplotlib, networkx, pyomo. Dev deps include jupyter-book and JupyterLab.
- Execution style: modules are intended to be run as scripts (they include example main-blocks) rather than used exclusively as importable packages. Running the file by path (python path\to\file.py) is the most reliable quick way to reproduce examples.
- Filesystem quirk: the code lives in a directory named `linkedin-games` (contains a hyphen). That makes dot-importing by package name tricky in some environments; prefer running scripts directly or install the project into the environment (`pip install -e .`).
- Visualization: each example's show() method depends on networkx + matplotlib and opens an interactive plot—use a GUI-capable environment or export plots non-interactively when running in CI.
- Jupyter Book workflow: the book uses the code examples in repo; ensure the environment (venv) has the listed dependencies before building.

5) Helpful quick pointers for Copilot-style sessions
- When asked to run or modify an example, search under linkedin-games/ for the module name and inspect its solve() to determine which solver is expected.
- If proposing changes that touch solver calls, call out licensing (gurobi) and suggest fallback to highs when appropriate.
- For doc changes, operate in `book/` and use `jupyter-book build --html` to verify output.

Other AI assistant configs
- No CLAUDE.md, AGENTS.md, CONVENTIONS.md, AIDER_CONVENTIONS.md, .windsurfrules, .cursorrules, or .clinerules detected.

---
If you want adjustments or coverage for additional areas (examples, packaging, CI), say which area to expand.