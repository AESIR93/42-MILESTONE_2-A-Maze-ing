#!/usr/bin/env python3

class Cell():
    def __init__(self, north: bool = True, south: bool = True,
                 west: bool = True, east: bool = True) -> None:
        self.north = north
        self.south = south
        self.west = west
        self.east = east


def render(maze: list[list[Cell]]) -> None:
    """Print the maze in the terminal.

    Args:
        maze: A list of list of Cell objects representing the maze.
    """
    for row in maze:
        line_top = ""
        for cell in row:
            line_top += "+"
            if cell.north:
                line_top += "--"
            else:
                line_top += "  "
        line_top += "+"
        print(line_top)
        line_side = ""
        for cell in row:
            if cell.west:
                line_side += "|  "
            else:
                line_side += "   "
        line_side += "|"
        print(line_side)
    last_row = maze[-1]
    line_bot = ""
    for cell in last_row:
        line_bot += "+--"
    line_bot += "+"
    print(line_bot)


def main() -> None:
    maze = [[Cell() for _ in range(8)] for _ in range(4)]
    maze[1][1].north = False
    maze[2][4].west = False
    maze[0][3].north = False
    maze[1][6].west = False
    maze[3][4].west = False
    render(maze)


if __name__ == "__main__":
    main()
