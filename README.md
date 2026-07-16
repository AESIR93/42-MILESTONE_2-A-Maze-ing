# A-Maze-ing

*This project has been created as part of the 42 curriculum by edsole-a, dhontani.*

---

## Description

A-Maze-ing is a Python 3 maze generator and terminal visualizer. It reads a configuration file, generates a random maze, renders it in ASCII in the terminal, and writes the maze to an output file in hexadecimal format together with the entry, exit, and shortest path.

The maze generator also supports a hidden "42" pattern when the maze size allows it, and the program can display the shortest path interactively. The project is split into two parts:
- The main program in `A-Maze-ing/` handles configuration, display, output, and user interaction.
- The reusable maze generation library in `mazegen/` can be installed and used independently.

---

## Instructions

### Requirements

- Python 3.10 or later
- pip

### Installation

```bash
make install
```

This installs the dependencies required by the terminal program. To build the reusable package from source, run:

```bash
cd mazegen
python -m build
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

The configuration file must contain one `KEY=VALUE` pair per line. Blank lines are ignored, and lines starting with `#` are treated as comments.

Supported keys:

| Key | Description | Example |
|---|---|---|
| `WIDTH` | Maze width in cells (integer > 0) | `WIDTH=20` |
| `HEIGHT` | Maze height in cells (integer > 0) | `HEIGHT=15` |
| `ENTRY` | Entry coordinates as `x,y` | `ENTRY=0,0` |
| `EXIT` | Exit coordinates as `x,y` | `EXIT=19,14` |
| `OUTPUT_FILE` | Name of the output file | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Whether the maze is perfect | `PERFECT=True` |
| `SEED` | Optional random seed for reproducible output | `SEED=42` |

A default `config.txt` is provided in the repository.

Example configuration:

```text
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

---

## Maze Generation Algorithm

The maze is generated using the Recursive Backtracker algorithm, which is a randomized depth-first search.

### How it works

1. Start at the entry cell and push it onto a stack.
2. Pick a random unvisited neighbour, remove the wall between them, and move to it.
3. If no unvisited neighbours exist, backtrack by popping the stack.
4. Repeat until the stack is empty, which means every reachable cell has been visited.

### Why this algorithm

Recursive Backtracker was chosen because it is simple to implement, easy to reason about, and produces long winding corridors that look good in a maze visualizer. It also matched the rest of the project well: the generator needed a clear path-solving step, support for reproducible output with a seed, and a structure that was easy to package into a reusable module.

---

## Advanced Features

The program includes a few interactive display options beyond simple generation:

- Regenerate a new maze without restarting the program.
- Show or hide the shortest path.
- Cycle through different wall colors in the terminal.
- Save the output file and quit from the interactive view.

These features are controlled from the keyboard after the maze is rendered.

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

## Output File Format

The output file contains:

1. The maze grid in hexadecimal — one row per line, one hex digit per cell. Each digit encodes which walls are closed using 4 bits: bit 0 = North, bit 1 = East, bit 2 = South, bit 3 = West. A closed wall sets the bit to 1.
2. A blank line.
3. The entry coordinates (`x,y`).
4. The exit coordinates (`x,y`).
5. The shortest path from entry to exit as a sequence of `N`, `E`, `S`, `W` characters.

---

## Reusable Module

The reusable part of the project is the `mazegen` package. It exposes the maze generator, the solved path, the grid representation, and conversion helpers for display code.

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
| edsole-a | maze generator, including the recursive backtracker logic, solver support, the "42" pattern, and hexadecimal output |
| dhontani | config parsing, ASCII renderer, user interactions, package structure, Makefile, and README |

### Planning

We started by splitting the project into two tracks: edsole-a focused on the reusable generator and maze-solving logic, while dhontani handled configuration parsing, terminal rendering, and project wiring. The initial plan was to finish generation first and then connect the display and file output around it.

That plan held up in broad strokes, but integration took longer than expected. The reusable module and terminal UI were straightforward separately, but getting the configuration, display, output format, and interactive controls to behave consistently required extra iteration. The README and packaging work also took longer than expected because we wanted the project to be easy to install and understand from the root of the repository.

### What worked well and what could be improved

What worked well was the clean split between generation and presentation: once the maze logic was isolated in `mazegen`, the main program became easier to maintain and reuse. The interactive terminal display also made it easy to test changes quickly.

What could be improved is earlier alignment on the final public API and output format. Some work was duplicated during integration because the generator, renderer, and config validation each evolved at slightly different speeds. Next time, we would lock down the interfaces sooner and leave more time for end-to-end testing and documentation.

### Tools used

- Python 3.10+
- VS Code
- Git / GitHub
- `flake8` and `mypy` for code quality
- `readchar` for terminal key input
- `python-build` for packaging

---

## Resources

AI was used to help draft and rewrite this README, to structure the required sections clearly, and to cross-check the documentation against the implemented code. It was also used to polish the wording for the configuration format, algorithm explanation, reusable module section, and the team-management summary.

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive Backtracker explained — Think Labyrinth](http://www.astrolog.org/labyrnth/algrithm.htm)
- [BFS and pathfinding — Red Blob Games](https://www.redblobgames.com/pathfinding/a-star/introduction.html)
- [Python packaging — official guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [ANSI escape codes — Wikipedia](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [mypy documentation](https://mypy.readthedocs.io/en/stable/)
- [flake8 documentation](https://flake8.pycqa.org/en/latest/)
- [readchar documentation](https://pypi.org/project/readchar/)
