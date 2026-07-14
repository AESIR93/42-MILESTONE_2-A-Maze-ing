#!/usr/bin/env python3

import readchar
from print_maze import render, path_to_coords
from parse_config import parse_config, dict_validation
from maze_generator import MazeGenerator
import sys
import os


def print_menu() -> None:
    print("\nChoose an option to interact with your maze!")
    print("Options:")
    print("     r: Regenerate maze")
    print("     p: Show/hide path")
    print("     c: Change color")
    print("     q: quit")
    print("Choose now: ", end="")
    sys.stdout.flush()


def main() -> None:
    config = parse_config(sys.argv[1])
    validated_dict = dict_validation(config)
    generator = MazeGenerator(
        width=validated_dict["WIDTH"],
        height=validated_dict["HEIGHT"],
        entry=validated_dict["ENTRY"],
        exit=validated_dict["EXIT"],
        perfect=validated_dict["PERFECT"]
    )
    generator.generate()
    cells = generator.to_cells()
    path = generator.solve()
    coords = path_to_coords(path, generator.entry)
    render(cells, coords)
    print_menu()
    show_path = True
    colors = ["\033[37m", "\033[31m", "\033[32m", "\033[34m"]
    color_idx = 0
    while True:
        key = readchar.readkey()
        if key == 'r':
            os.system("clear")
            generator.generate()
            cells = generator.to_cells()
            path = generator.solve()
            coords = path_to_coords(path, generator.entry)
            render(cells, coords)
            print_menu()
        elif key == 'p':
            os.system("clear")
            if show_path is True:
                show_path = False
                render(cells)
                print_menu()
            elif show_path is False:
                show_path = True
                render(cells, coords)
                print_menu()
        elif key == 'c':
            os.system("clear")
            color_idx = (color_idx + 1) % len(colors)
            if show_path is True:
                render(cells, coords, colors[color_idx])
                print_menu()
            elif show_path is False:
                render(cells, None, colors[color_idx])
                print_menu()
        elif key == 'q':
            sys.exit()


if __name__ == "__main__":
    main()
