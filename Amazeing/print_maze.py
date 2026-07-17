#!/usr/bin/env python3

from maze_generator import Cell
import time

def render_path(coords: list[tuple[int, int]], animate: bool = True) -> None:
    if animate is True:
        for x, y in coords[1:-1]:
            fila = y * 2 + 2
            columna = x * 3 + 2
            print(f"\033[{fila};{columna}H\033[1;93m*\033[0m", end="", flush=True)
            time.sleep(0.02)
    else:
        for x, y in coords[1:-1]:
            fila = y * 2 + 2
            columna = x * 3 + 2
            print(f"\033[{fila};{columna}H\033[1;93m*\033[0m", end="", flush=True)


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
           path_coords: list[tuple[int, int]] = None,
           wall_color: str = "\033[1;95m") -> None:
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
                if ((x, y) == path_coords[0]):
                    line_side += f"{wall_color}║\033[1;92m▓\033[0m\033[1;38;5;22m»\033[0m"
                elif (x, y) == path_coords[len(path_coords) - 1]:
                    line_side += f"{wall_color}║\033[1;91m»\033[0m\033[1;38;5;202m▓\033[0m"
                else:
                    line_side += f"{wall_color}║  \033[0m"
            else:
                if ((x, y) == path_coords[0]):
                    line_side += f"{wall_color}\033[1;92m▓\033[0m\033[1;38;5;22m»\033[0m "
                elif (x, y) == path_coords[len(path_coords) - 1]:
                    line_side += f"{wall_color}\033[1;91m»\033[0m\033[1;38;5;202m▓\033[0m "
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
