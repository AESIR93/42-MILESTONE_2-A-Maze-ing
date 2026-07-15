# A-Maze-ing

*This project has been created as part of the 42 curriculum by edsole, dhontani.*

---

## Description

A-Maze-ing is a maze generator written in Python 3. Given a configuration file, it generates a random maze, displays it in the terminal with ASCII rendering, and writes the result to an output file in hexadecimal format. The maze includes a hidden "42" pattern and supports finding and displaying the shortest path from the entry to the exit.

The project is split into two parts:
- The main program (`a_maze_ing.py`) handles configuration, display, and user interaction.
- The reusable maze generation library (`mazegen`) can be installed independently via pip.

---

## Instructions

### Requirements

- Python 3.10 or later
- pip

### Installation

```bash
make install
```

### Running the program

```bash
python3 a_maze_ing.py config.txt
```

Or via the Makefile:

```bash
make run
```

### Other Makefile targets

```bash
make debug    # Run with Python debugger (pdb)
make clean    # Remove caches and temporary files
make lint     # Run flake8 and mypy
```

---

## Configuration File Format

The configuration file must contain one `KEY=VALUE` pair per line. Lines starting with `#` are treated as comments and ignored.

| Key | Description | Example |
|---|---|---|
| `WIDTH` | Maze width in cells (integer > 0) | `WIDTH=20` |
| `HEIGHT` | Maze height in cells (integer > 0) | `HEIGHT=15` |
| `ENTRY` | Entry coordinates as `x,y` | `ENTRY=0,0` |
| `EXIT` | Exit coordinates as `x,y` | `EXIT=19,14` |
| `OUTPUT_FILE` | Name of the output file | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Whether the maze is perfect | `PERFECT=True` |

A default `config.txt` is provided in the repository.

---

## User Interactions

Once the maze is displayed, the following keys are available:

| Key | Action |
|---|---|
| `r` | Regenerate a new maze |
| `p` | Show / hide the shortest path |
| `c` | Cycle through wall colours |
| `q` | Save output file and quit |

---

## Maze Generation Algorithm

The maze is generated using the **Recursive Backtracker** algorithm (also known as randomised DFS).

### How it works

1. Start at the entry cell and push it onto a stack.
2. Pick a random unvisited neighbour, remove the wall between them, and move to it.
3. If no unvisited neighbours exist, backtrack by popping the stack.
4. Repeat until the stack is empty — every cell has been visited.

### Why this algorithm

[**Fill in here**: explain in your own words why you chose Recursive Backtracker over Prim's or Kruskal's — e.g. simplicity of implementation, quality of the generated mazes, familiarity with DFS from other projects, etc.]

---

## Output File Format

The output file contains:

1. The maze grid in hexadecimal — one row per line, one hex digit per cell. Each digit encodes which walls are closed using 4 bits: bit 0 = North, bit 1 = East, bit 2 = South, bit 3 = West. A closed wall sets the bit to 1.
2. A blank line.
3. The entry coordinates (`x,y`).
4. The exit coordinates (`x,y`).
5. The shortest path from entry to exit as a sequence of `N`, `E`, `S`, `W` characters.

---

## Reusable Module

The maze generation logic is packaged as a standalone installable library called `mazegen`.

### Installing the package

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Basic usage

```python
from mazegen.maze_generator import MazeGenerator

gen = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    seed=42,         # optional, for reproducibility
    perfect=True     # optional, default True
)

gen.generate()

# Access the grid (list of lists of ints, hex-encoded walls)
grid = gen.grid

# Get the grid as a hex string (output file format)
hex_str = gen.get_hex_string()

# Get the shortest path as a list of directions
path = gen.solve()  # e.g. ['E', 'E', 'S', 'N', ...]

# Get the maze as Cell objects (for display)
cells = gen.to_cells()
```

### Rebuilding the package from source

```bash
cd mazegen
pip install build
python -m build
# Output: dist/mazegen-1.0.0-py3-none-any.whl
```

---

## Team and Project Management

### Roles

| Member | Role |
|---|---|
| edsole | [**Fill in**: e.g. maze generation algorithm, BFS solver, "42" pattern, package structure] |
| dhontani | [**Fill in**: e.g. config parser, ASCII renderer, user interactions, hex output, Makefile] |

### Planning

[**Fill in**: describe your initial plan, how you divided the work, and how the timeline evolved. What did you finish earlier or later than expected?]

### What worked well and what could be improved

[**Fill in**: e.g. communication, design decisions that paid off, things you would do differently, technical debt, etc.]

### Tools used

- Python 3.10+
- VSCode
- Git / GitHub
- `flake8`, `mypy` for code quality
- `readchar` for terminal key input
- `python-build` for packaging
- Claude (Anthropic) — [**Fill in**: describe specifically which tasks you used AI for and how you validated the output]

---

## Resources

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive Backtracker explained — Think Labyrinth](http://www.astrolog.org/labyrnth/algrithm.htm)
- [BFS and pathfinding — Red Blob Games](https://www.redblobgames.com/pathfinding/a-star/introduction.html)
- [Python packaging — official guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [ANSI escape codes — Wikipedia](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [mypy documentation](https://mypy.readthedocs.io/en/stable/)
- [flake8 documentation](https://flake8.pycqa.org/en/latest/)
