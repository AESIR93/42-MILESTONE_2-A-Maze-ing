from typing import Optional
from collections import deque
import random
import sys


class Cell:
    """Single maze cell, exposed for display/consumer code.

        Attributes:
            north: True if the north wall is closed.
            south: True if the south wall is closed.
            west:  True if the west wall is closed.
            east:  True if the east wall is closed.
        """

    def __init__(self, north: bool = True, south: bool = True,
                 west: bool = True, east: bool = True) -> None:
        self.north = north
        self.south = south
        self.west = west
        self.east = east


NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000

ALL_WALLS = NORTH | EAST | SOUTH | WEST

_PATTERN_42: list[str] = [
    "1001 1111",
    "1001 0001",
    "1111 1111",
    "0001 1000",
    "0001 1111",
]
_PATTERN_HEIGHT: int = len(_PATTERN_42)
_PATTERN_WIDTH: int = len(_PATTERN_42[0])


class MazeGenerator:
    """Generates a 2D maze using recursive backtracker (DFS).

    Args:
        width:   Number of cells horizontally.
        height:  Number of cells vertically.
        entry:   (x, y) of the entry cell.
        exit:    (x, y) of the exit cell.
        seed:    RNG seed for reproducibility. None = random.
        perfect: If True, exactly one path exists between any two cells.
    """

    def __init__(self,
                 width: int,
                 height: int,
                 entry: tuple[int, int],
                 exit: tuple[int, int],
                 seed: Optional[int] = None,
                 perfect: bool = True) -> None:
        self._validate_params(width, height, entry, exit)
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.seed = seed
        self.perfect = perfect
        self.grid: list[list[int]] = []
        self._pattern_cells: set[tuple[int, int]] = set()

    def _validate_params(self,
                         width: int,
                         height: int,
                         entry: tuple[int, int],
                         exit: tuple[int, int]) -> None:
        """Validate constructor parameters.

        Args:
            width:  Maze width.
            height: Maze height.
            entry:  Entry cell coordinates.
            exit:   Exit cell coordinates.

        Raises:
            ValueError: If any parameter is invalid.
        """
        if width < 2 or height < 2:
            raise ValueError("Maze dimensions must be at least 2x2.")
        ex, ey = entry
        xx, xy = exit
        if not (0 <= ex < width and 0 <= ey < height):
            raise ValueError(f"Entry {entry} is out of bounds.")
        if not (0 <= xx < width and 0 <= xy < height):
            raise ValueError(f"Exit {exit} is out of bounds.")
        if entry == exit:
            raise ValueError("Entry and exit must be different cells.")

    def _pattern_shape(self) -> set[tuple[int, int]]:
        """Compute the raw '42' pattern cell coordinates.

        Pure geometry: assumes the maze is already known to be big
        enough to hold the pattern. Callers must check the size
        first.

        Returns:
            Set of (x, y) coordinates belonging to the pattern.
        """
        start_x = (self.width - _PATTERN_WIDTH) // 2
        start_y = (self.height - _PATTERN_HEIGHT) // 2
        cells: set[tuple[int, int]] = set()

        for dy, row in enumerate(_PATTERN_42):
            for dx, char in enumerate(row):
                if char == "1":
                    cells.add((start_x + dx, start_y + dy))

        return cells

    def _pattern_creates_pocket(self, pattern: set[tuple[int, int]]) -> bool:
        """Check whether excluding `pattern` isolates other cells.

        The '42' pattern is the only thing allowed to be isolated
        in the maze. If its shape happens to fully enclose one or
        more ordinary cells, those cells could never be reached by
        the backtracker and would stay disconnected forever. This
        walks the free-cell grid (ignoring maze walls, only cell
        adjacency) from the entry to check every other free cell
        is reachable through free neighbours alone.

        Args:
            pattern: Candidate pattern cell coordinates.

        Returns:
            True if at least one non-pattern cell is unreachable
            from the entry, False otherwise.
        """
        seen: set[tuple[int, int]] = {self.entry}
        stack: list[tuple[int, int]] = [self.entry]
        while stack:
            x, y = stack.pop()
            for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                nx, ny = x + dx, y + dy
                if not (0 <= nx < self.width and 0 <= ny < self.height):
                    continue
                if (nx, ny) in seen or (nx, ny) in pattern:
                    continue
                seen.add((nx, ny))
                stack.append((nx, ny))
        free_total = self.width * self.height - len(pattern)
        return len(seen) != free_total

    def _resolve_pattern_cells(self) -> set[tuple[int, int]]:
        """Compute the '42' pattern cells, or safely omit them.

        The pattern is omitted (with a message on stderr) instead
        of letting the whole generation fail whenever including it
        would make the maze invalid: too small to hold it,
        overlapping the entry/exit, or boxing in ordinary cells so
        they could never connect to the rest of the maze.

        Returns:
            Set of (x, y) coordinates in the pattern, or an empty
            set if it had to be omitted.
        """
        if self.width < _PATTERN_WIDTH or self.height < _PATTERN_HEIGHT:
            print(
                "Warning: maze too small to display the '42' "
                "pattern; omitting it.",
                file=sys.stderr)
            return set()

        pattern = self._pattern_shape()

        if self.entry in pattern or self.exit in pattern:
            print(
                "Warning: '42' pattern overlaps the entry/exit for "
                "this configuration; omitting it.",
                file=sys.stderr)
            return set()

        if self._pattern_creates_pocket(pattern):
            print(
                "Warning: '42' pattern would isolate some cells "
                "for this maze size; omitting it.",
                file=sys.stderr)
            return set()

        return pattern

    def generate(self) -> list[list[int]]:
        """Generate the maze using recursive backtracking.

        If the '42' pattern cannot be placed for this maze's size
        (too small, overlapping the entry/exit, or would isolate
        other cells), it is omitted and a message is printed to
        stderr instead of failing the whole generation.

        Returns:
            The generated grid.
        """
        self.grid = [
            [ALL_WALLS for _ in range(self.width)]
            for _ in range(self.height)
        ]
        visited = [
            [False for _ in range(self.width)]
            for _ in range(self.height)
        ]

        rng = random.Random(self.seed)

        self._pattern_cells = self._resolve_pattern_cells()

        for px, py in self._pattern_cells:
            visited[py][px] = True

        ex, ey = self.entry
        visited[ey][ex] = True
        stack: list[tuple[int, int]] = [self.entry]

        while stack:
            x, y = stack[-1]
            neighbours: list[tuple[int, int]] = []

            if y > 0 and not visited[y - 1][x]:
                neighbours.append((x, y - 1))
            if x < self.width - 1 and not visited[y][x + 1]:
                neighbours.append((x + 1, y))
            if y < self.height - 1 and not visited[y + 1][x]:
                neighbours.append((x, y + 1))
            if x > 0 and not visited[y][x - 1]:
                neighbours.append((x - 1, y))

            if neighbours:
                nx, ny = rng.choice(neighbours)
                self._remove_wall(x, y, nx, ny)
                visited[ny][nx] = True
                stack.append((nx, ny))
            else:
                stack.pop()

        if not self.perfect:
            self._add_loops(rng)

        if not self.validate_corridor_width():
            raise RuntimeError(
                "internal error: corridor wider than 2 cells")
        if self.perfect and not self.is_perfect():
            raise RuntimeError(
                "internal error: perfect maze has multiple paths")

        return self.grid

    def _add_loops(self, rng: random.Random) -> None:
        """Remove walls to introduce loops (imperfect maze).

        Targets ~10% of removable internal walls while respecting
        the corridor-width constraint. Reverts any removal that
        creates a 3x3 open area.

        Args:
            rng: Seeded random number generator.
        """
        candidates: list[tuple[int, int, int, int]] = []

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self._pattern_cells:
                    continue
                if (x < self.width - 1
                        and (x + 1, y) not in self._pattern_cells
                        and self.grid[y][x] & EAST):
                    candidates.append((x, y, x + 1, y))
                if (y < self.height - 1
                        and (x, y + 1) not in self._pattern_cells
                        and self.grid[y][x] & SOUTH):
                    candidates.append((x, y, x, y + 1))

        rng.shuffle(candidates)
        target = max(1, len(candidates) // 10)
        removed = 0

        for x, y, nx, ny in candidates:
            if removed >= target:
                break
            self._remove_wall(x, y, nx, ny)
            if not self.validate_corridor_width():
                if nx == x + 1:
                    self.grid[y][x] |= EAST
                    self.grid[ny][nx] |= WEST
                else:
                    self.grid[y][x] |= SOUTH
                    self.grid[ny][nx] |= NORTH
            else:
                removed += 1

    def _remove_wall(self, x: int, y: int, nx: int, ny: int) -> None:
        """Remove the wall between two adjacent cells.

        Args:
            x:  X-coordinate of the current cell.
            y:  Y-coordinate of the current cell.
            nx: X-coordinate of the neighbouring cell.
            ny: Y-coordinate of the neighbouring cell.

        Raises:
            ValueError: If the cells are not orthogonally adjacent.
        """
        if nx == x and ny == y - 1:
            self.grid[y][x] &= ~NORTH
            self.grid[ny][nx] &= ~SOUTH
        elif nx == x and ny == y + 1:
            self.grid[y][x] &= ~SOUTH
            self.grid[ny][nx] &= ~NORTH
        elif nx == x + 1 and ny == y:
            self.grid[y][x] &= ~EAST
            self.grid[ny][nx] &= ~WEST
        elif nx == x - 1 and ny == y:
            self.grid[y][x] &= ~WEST
            self.grid[ny][nx] &= ~EAST
        else:
            raise ValueError("Cells are not adjacent.")

    def is_perfect(self) -> bool:
        """Validate that the maze is perfect.

        A perfect maze has exactly one path between any two cells
        (i.e. it is a spanning tree). Pattern cells are excluded
        from the cell count since they are intentionally isolated.

        Returns:
            True if the maze is perfect, False otherwise.
        """
        if not self.is_fully_connected():
            return False

        total_passages = 0
        for row in self.grid:
            for cell_value in row:
                total_passages += 4 - bin(cell_value).count('1')
        total_passages //= 2

        effective = self.width * self.height - len(self._pattern_cells)
        return total_passages == effective - 1

    def is_fully_connected(self) -> bool:
        """Check if all non-pattern cells are reachable from entry.

        Returns:
            True if all reachable cells are connected, False otherwise.
        """
        visited: set[tuple[int, int]] = set()
        queue: deque[tuple[int, int]] = deque([self.entry])
        visited.add(self.entry)

        while queue:
            x, y = queue.popleft()
            cell_value = self.grid[y][x]

            if (not (cell_value & NORTH) and y > 0
                    and (x, y - 1) not in visited):
                visited.add((x, y - 1))
                queue.append((x, y - 1))
            if (not (cell_value & EAST) and x < self.width - 1
                    and (x + 1, y) not in visited):
                visited.add((x + 1, y))
                queue.append((x + 1, y))
            if (not (cell_value & SOUTH) and y < self.height - 1
                    and (x, y + 1) not in visited):
                visited.add((x, y + 1))
                queue.append((x, y + 1))
            if (not (cell_value & WEST) and x > 0
                    and (x - 1, y) not in visited):
                visited.add((x - 1, y))
                queue.append((x - 1, y))

        expected = self.width * self.height - len(self._pattern_cells)
        return len(visited) == expected

    def solve(self) -> list[str]:
        """Find the shortest path from entry to exit using BFS.

        Returns:
            List of direction characters ('N', 'E', 'S', 'W')
            representing the shortest path from entry to exit.

        Raises:
            ValueError: If the maze has not been generated or
                        no path exists between entry and exit.
        """
        if not self.grid:
            raise ValueError("Maze has not been generated yet.")

        dirs: list[tuple[int, int, int, str]] = [
            (0, -1, NORTH, 'N'),
            (1,  0, EAST,  'E'),
            (0,  1, SOUTH, 'S'),
            (-1, 0, WEST,  'W'),
        ]

        parent: dict[
            tuple[int, int],
            Optional[tuple[tuple[int, int], str]]
        ] = {self.entry: None}
        queue: deque[tuple[int, int]] = deque([self.entry])

        while queue:
            x, y = queue.popleft()
            if (x, y) == self.exit:
                break
            for dx, dy, wall_bit, direction in dirs:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width
                    and 0 <= ny < self.height
                    and not (self.grid[y][x] & wall_bit)
                        and (nx, ny) not in parent):
                    parent[(nx, ny)] = ((x, y), direction)
                    queue.append((nx, ny))

        if self.exit not in parent:
            raise ValueError(
                "No path exists between entry and exit."
            )

        path: list[str] = []
        current: tuple[int, int] = self.exit
        while True:
            record = parent[current]
            if record is None:
                break
            prev_cell, direction = record
            path.append(direction)
            current = prev_cell

        path.reverse()
        return path

    def to_cells(self) -> list[list[Cell]]:
        """Convert the internal grid format to Cell objects.

        Returns:
            A 2D list of Cell objects with walls set per the grid.
        """
        cells: list[list[Cell]] = []
        for y in range(self.height):
            row: list[Cell] = []
            for x in range(self.width):
                cell_value = self.grid[y][x]
                row.append(Cell(
                    north=bool(cell_value & NORTH),
                    south=bool(cell_value & SOUTH),
                    east=bool(cell_value & EAST),
                    west=bool(cell_value & WEST),
                ))
            cells.append(row)
        return cells

    def get_hex_string(self) -> str:
        """Convert maze grid to hexadecimal string representation.

        Each cell is one uppercase hex digit encoding closed walls.

        Returns:
            Uppercase hex string, one row per line, each ending
            with a newline.
        """
        lines: list[str] = []
        for row in self.grid:
            lines.append("".join(format(v, 'X') for v in row))
        return "\n".join(lines) + "\n"

    def validate_corridor_width(self) -> bool:
        """Check that no 3x3 area is fully passable.

        A 3x3 block is invalid if every internal horizontal and
        vertical passage within it is open (no walls separating
        any adjacent pair of cells in the block).

        Returns:
            True if no such area exists, False otherwise.
        """
        for y in range(self.height - 2):
            for x in range(self.width - 2):
                h_open = all(
                    not (self.grid[y + dy][x + dx] & EAST)
                    for dy in range(3)
                    for dx in range(2)
                )
                if not h_open:
                    continue
                v_open = all(
                    not (self.grid[y + dy][x + dx] & SOUTH)
                    for dy in range(2)
                    for dx in range(3)
                )
                if v_open:
                    return False
        return True
