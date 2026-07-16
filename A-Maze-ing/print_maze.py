#!/usr/bin/env python3

from maze_generator import Cell
from typing import Optional


def path_to_coords(path: list[str],
                   entry: tuple[int, int]) -> list[tuple[int, int]]:
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


def render(maze: list[list[Cell]],
           path_coords: Optional[list[tuple[int, int]]] = None,
           wall_color: str = "\033[1;96m") -> None:
    """Print the maze in the terminal.

    Args:
        maze: A list of list of Cell objects representing the maze.
    """
    for y, row in enumerate(maze):
        line_top = ""
        for x, cell in enumerate(row):
            line_top += f"{wall_color}¤\033[0m"
            if cell.north and cell.south and cell.east and cell.west:
                line_top += "\033[1;92m##\033[0m"
            elif cell.north:
                line_top += f"{wall_color}══\033[0m"
            else:
                line_top += "  "
        line_top += f"{wall_color}¤\033[0m"
        print(line_top)
        line_side = ""
        for x, cell in enumerate(row):
            if cell.north and cell.south and cell.east and cell.west:
                line_side += "\033[1;92m║██\033[0m"
            elif cell.west:
                if (path_coords and (x, y) == path_coords[0]
                    or path_coords
                        and (x, y) == path_coords[len(path_coords) - 1]):
                    line_side += f"{wall_color}║\033[1;91m×\033[0m "
                elif path_coords and (x, y) in path_coords:
                    line_side += f"{wall_color}║\033[1;93m*\033[0m "
                else:
                    line_side += f"{wall_color}║  \033[0m"
            else:
                if (path_coords and (x, y) == path_coords[0]
                        or path_coords
                        and (x, y) == path_coords[len(path_coords) - 1]):
                    line_side += f"{wall_color} \033[1;91m×\033[0m "
                elif path_coords and (x, y) in path_coords:
                    line_side += " \033[1;93m*\033[0m "
                else:
                    line_side += "   "
        line_side += f"{wall_color}║\033[0m"
        print(line_side)
    last_row = maze[-1]
    line_bot = ""
    for cell in last_row:
        line_bot += f"{wall_color}¤══\033[0m"
    line_bot += f"{wall_color}¤\033[0m"
    print(line_bot)
