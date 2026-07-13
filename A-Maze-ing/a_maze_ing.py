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
            pass
        elif key == 'c':
            pass
        elif key == 'q':
            sys.exit()


if __name__ == "__main__":
    main()
