from typing import Optional

NORTH = 0b0001
EAST = 0b0010
SOUTH = 0b0100
WEST = 0b1000

ALL_WALLS = NORTH | EAST | SOUTH | WEST


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
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.seed = seed
        self.perfect = perfect
