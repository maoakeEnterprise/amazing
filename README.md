This project has been created as part of the 42 curriculum by *mteriier*, *dgaillet*

# A-Maze-ing

## Description

A-Maze-ing is a Python project that generates, solves, exports, and displays mazes.

The program:

- reads a configuration file,
- generates a maze according to the requested parameters,
- optionally enforces a **perfect maze** property,
- solves the maze from entry to exit,
- writes the maze to an output file using the required hexadecimal wall encoding,
- and displays the maze visually through an **MLX graphical window**.

This project was designed with **code reusability** in mind.  
The maze generation and solving logic is exposed through a reusable Python package named **`mazegen`**, which can be built and installed independently for use in future projects.

---

## Features

- Maze generation from a config file
- Multiple generation algorithms:
  - `DFS` (depth-first search / recursive backtracking style)
  - `Kruskal`
- Multiple solving algorithms:
  - `AStar`
  - `DFS`
- Perfect and imperfect maze support
- Maze export using hexadecimal wall encoding
- Graphical rendering with MLX
- Animated generation
- Animated solution path display
- Wall color switching
- Reserved visual **“42” pattern** using fully closed cells when the maze is large enough
- Reusable `mazegen` package

---

## Project Structure

```text
.
├── a_maze_ing.py          # Main executable script and MLX display
├── config.txt             # Default configuration file
├── Makefile
├── README.md
├── src/
│   ├── AMazeIng.py
│   ├── mazegen/
│   │   ├── __init__.py
│   │   ├── Cell.py
│   │   ├── Maze.py
│   │   ├── MazeGenerator.py
│   │   └── MazeSolver.py
│   └── parsing/
│       └── Parsing.py
└── tests/
```

---

## Instructions

### Requirements

- Python **3.10+**
- `uv`, `pip`
- MLX Python binding used by the project

### Installation

Using the provided `Makefile`:

```bash
make install
```

This installs project dependencies and the MLX wheel used by the graphical display.

---

## Run

```bash
make run
```

---

## Debug

```bash
make debug
```

---

## Lint

Mandatory lint target:

```bash
make lint
```

Strict lint target:

```bash
make lint-strict
```

---

## Clean

```bash
make clean
```

Full cleanup:

```bash
make fclean
```

---

## Configuration File Format

The configuration file contains one `KEY=VALUE` pair per line.

### Mandatory keys

| Key | Description | Example |
|---|---|---|
| `WIDTH` | Maze width in cells | `WIDTH=20` |
| `HEIGHT` | Maze height in cells | `HEIGHT=15` |
| `ENTRY` | Entry coordinates `(x,y)` | `ENTRY=1,1` |
| `EXIT` | Exit coordinates `(x,y)` | `EXIT=20,15` |
| `OUTPUT_FILE` | Output filename | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Perfect maze or not | `PERFECT=True` |
| `GENERATOR` | Generation algorithm | `GENERATOR=DFS` |
| `SOLVER` | Solving algorithm | `SOLVER=AStar` |

### Supported values

#### GENERATOR

- `DFS`
- `Kruskal`

#### SOLVER

- `AStar`
- `DFS`

#### PERFECT

- `True`
- `False`

### Example config

```ini
WIDTH=20
HEIGHT=15
ENTRY=1,1
EXIT=20,15
OUTPUT_FILE=maze.txt
PERFECT=True
GENERATOR=DFS
SOLVER=AStar
SEED=31766516
```

### Notes

- Coordinates are handled as tuples in the form `x,y`.
- In the current implementation, coordinates are expected to be **inside maze bounds**.
- Entry and exit must be valid cells.
- The parser validates required keys and converts values to the correct Python types.
- You can add a `SEED` value

---

## Output File Format

The generated maze is written row by row using **one hexadecimal digit per cell**.

Each cell stores wall information using this bitmask:

| Bit | Direction |
|---|---|
| `1` | North |
| `2` | East |
| `4` | South |
| `8` | West |

A bit set to `1` means the wall is **closed**.

### Example

- `3` = `0011` → north and east closed
- `A` = `1010` → east and west closed

### Output layout

```text
<maze row 1>
<maze row 2>
...
<maze row n>

<entry coordinates>
<exit coordinates>
<solution path>
```

Example:

```text
FFFF
9A63
8C47
FFFF

1,1
4,4
EESSEN
```

---

## Visual Representation

This project provides a graphical rendering through **MLX**.

The display shows:

- maze walls,
- entry cell,
- exit cell,
- optional shortest path,
- reserved “42” pattern when present.

### Controls

In the MLX window:

- `1` / mapped equivalent: regenerate maze
- `2` / mapped equivalent: show/hide path
- `3` / mapped equivalent: change wall color
- `4` / mapped equivalent: quit

The code includes two key mappings to handle platform/layout differences.

### Visual Features

- animated generation,
- animated path display,
- color cycling for walls,
- separate color cycling for the “42” cells.

---

## Maze Generation Algorithm

This project supports two generation algorithms.

### 1. Depth-First Search (DFS)

This algorithm starts from a cell and repeatedly visits an unvisited neighbour, removing walls as it advances. When it reaches a dead end, it backtracks until it finds a cell with an unvisited neighbour.

#### Why this algorithm was chosen

- simple to implement,
- naturally produces connected mazes,
- works well for animation,
- produces visually interesting long corridors,
- easy to adapt for perfect mazes.

### 2. Kruskal

This algorithm treats each cell as its own set and removes walls between cells only when it connects two different sets. This avoids cycles and guarantees connectivity.

#### Why this algorithm was included

- classic maze generation algorithm,
- good complement to DFS,
- demonstrates modularity and algorithm interchangeability,
- naturally fits the reusable package requirement.

---

## Why These Algorithms Were Chosen

We chose DFS and Kruskal because together they provide:

- two well-known and complementary approaches,
- good pedagogical value,
- simple integration into a reusable class-based architecture,
- deterministic structure when used with a seed,
- compatibility with perfect maze generation.

DFS is particularly suitable for progressive visual rendering.  
Kruskal is useful to show a different construction logic based on set merging.

---

## Perfect and Imperfect Mazes

When `PERFECT=True`:

- the maze is generated as a **perfect maze**,
- there is exactly one path between any two reachable cells,
- in particular, entry and exit have a unique valid path.

When `PERFECT=False`:

- additional walls may be removed after initial generation,
- loops can appear,
- the maze remains connected,
- the solver still computes a valid path.

---

## The “42” Pattern

For sufficiently large mazes, the generator reserves a group of fully closed cells to draw a visible **“42”** pattern in the visual rendering.

### Behaviour

- the pattern is added only if the maze is large enough,
- if the maze is too small, the pattern may be omitted,
- this should be reported to the user with a console message.

### Current implementation note

The current code includes support for reserving and rendering the “42” pattern using cells with value `15` (all walls closed).  
The pattern is drawn in the central area when dimensions are large enough.

---

## Error Handling

The project is designed to fail gracefully and provide clear messages for common problems such as:

- missing configuration file,
- empty file,
- missing or invalid keys,
- invalid boolean values,
- invalid coordinates,
- invalid maze dimensions,
- solving an uninitialized maze.

The parser catches several common exceptions and prints user-friendly messages before exiting.

---

## Reusable Code

The reusable part of the project is the **`mazegen`** package.

It contains:

- `Cell`: wall bitmask representation,
- `Maze`: maze container and textual/ascii rendering,
- `MazeGenerator`: abstract generator interface,
- `DepthFirstSearch`: DFS-based maze generator,
- `Kruskal`: Kruskal-based maze generator,
- `MazeSolver`: abstract solver interface,
- `AStar`: shortest-path solver,
- `DepthFirstSearchSolver`: DFS-based path solver.

This package can be built as a wheel and reused independently of the MLX application.

---

## How to Use the Reusable Module

### Basic example

```python
from mazegen import Maze
from mazegen import DepthFirstSearch, AStar

generator = DepthFirstSearch(start=(1, 1), end=(10, 10), perfect=True)
solver = AStar(start=(1, 1), end=(10, 10))

maze = Maze()

for grid in generator.generator(height=10, width=10, seed=42):
    maze.set_maze(grid)

path = solver.solve(maze, height=10, width=10)

print(maze)
print(path)
```

### With Kruskal

```python
from mazegen import Maze, Kruskal, AStar

generator = Kruskal(start=(1, 1), end=(20, 15), perfect=True)
solver = AStar(start=(1, 1), end=(20, 15))

maze = Maze()

for grid in generator.generator(height=15, width=20, seed=123):
    maze.set_maze(grid)

print(solver.solve(maze, height=15, width=20))
```

### Accessing the generated structure

```python
maze_array = maze.get_maze()
```

Each element of `maze_array` is a `Cell` object exposing:

- `get_north()`
- `get_est()`
- `get_south()`
- `get_west()`
- `get_value()`

### Accessing a solution

```python
solution = solver.solve(maze, height=15, width=20)
print(solution)  # Example: "EESSWN..."
```

---

## Packaging

The reusable package is distributed as **`mazegen-*`**.

Example expected artifact:

```text
mazegen-1.0.0-py3-none-any.whl
```

Build with:

```bash
make build
```

This produces a wheel suitable for later installation with `pip`/`uv`.

---

## Tests

Unit tests are recommended and partially integrated through `pytest` targets in the Makefile.

Start test with:

```bash
make run_test
```

These tests are useful to validate:

- parsing,
- generation,
- solver behavior,
- edge cases.

---

## Technical Choices

### Language

- Python 3.10+

### Libraries

- `numpy` for grid storage
- `pydantic` for model validation
- `mlx` for graphical rendering
- `pytest` for tests
- `mypy` for static typing
- `flake8` for style checking

### Architecture

The project is separated into three main parts:

1. **Main application**
   - parsing,
   - orchestration,
   - MLX rendering,
   - user interaction.

2. **Domain model**
   - `AMazeIng`,
   - maze configuration and lifecycle.

3. **Reusable package**
   - generation,
   - solving,
   - maze structure.

This separation makes the generation logic portable to other projects.

---

## Team and Project Management

### Team roles

- **mteriier**
  - Parsing
  - DFS generator / solver
  - Makefile
  - some pytest
  - Fix of mazegen package generation
  - MLX
- **dgaillet**
  - AMazeIng config class
  - AStar solver
  - Kruskal generator
  - some pytest
  - mazegen package generation
  - MLX
  - Cell / Maze class

### Initial planning

Our initial plan was:

1. define the maze data model,
2. implement one working generation algorithm,
3. export the maze to the required format,
4. implement solving,
5. add graphical rendering,
6. package reusable code,
7. write tests and documentation.

### How planning evolved

In practice:

- the reusable package structure had to be stabilized earlier than expected,
- coordinate handling between parser, generator, solver, and renderer required extra work,
- rendering and animation took longer than planned,
- algorithm modularity made later integration easier.

### What worked well

- clean separation between generation and display,
- abstract base classes for generator and solver,
- Makefile automation,
- packaging the reusable module.

### What could be improved

- stricter normalization of coordinate conventions,
- seed support should be exposed directly from configuration,
- more tests for edge cases and invalid inputs,

### Tools used

- Git
- `uv`
- `flake8`
- `mypy`
- `pytest`
- MLX
- optionally AI assistance for docstrings, README

---

## Resources

### Documentation and references

- [NumPy Documentation](https://numpy.org/doc/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [A* Pathfinding explanation](https://matteo-tosato7.medium.com/exploring-the-depths-solving-mazes-with-a-search-algorithm-c15253104899)
- [Kruskal generation](https://medium.com/@anushidesilva28/understanding-kruskals-algorithm-44886bf8ba8b)

### How AI was used

AI was used as an assistant for:

- improving docstrings,
- helping structure the README,

---

## Reusable Module Summary

If you only want the reusable maze engine:

1. build/install `mazegen`,
2. import a generator and a solver,
3. generate a maze,
4. solve it,
5. access the grid through `Maze.get_maze()`.

This part is intended for reuse in future Python projects.
