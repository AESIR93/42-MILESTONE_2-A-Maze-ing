#!/usr/bin/env python3

from maze_generator import Cell
from typing import Optional


def path_to_coords(path: list[str], entry: tuple[int, int]) -> list[tuple[int, int]]:
    result = []
    x, y = entry
    result.append((x, y))
    for coord in path:
        if coord == 'N':
            y -= 1
        elif coord == 'S':
            y += 1
        elif coord == 'E':
            x += 1
        elif coord == 'W':
            x -= 1
        result.append((x, y))
    return result


def render(maze: list[list[Cell]], path_coords: Optional[list[tuple[int, int]]] = None) -> None:
    """Print the maze in the terminal.

    Args:
        maze: A list of list of Cell objects representing the maze.
    """
    for y, row in enumerate(maze):
        line_top = ""
        for x, cell in enumerate(row):
            line_top += "+"
            if cell.north:
                line_top += "--"
            else:
                line_top += "  "
        line_top += "+"
        print(line_top)
        line_side = ""
        for x, cell in enumerate(row):
            if cell.west:
                if path_coords and (x, y) in path_coords:
                    line_side += "|\033[33m+\033[0m "
                else:
                    line_side += "|  "
            else:
                if path_coords and (x, y) in path_coords:
                    line_side += " \033[33m+\033[0m "
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