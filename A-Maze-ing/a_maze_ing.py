#!/usr/bin/env python3

import readchar
from print_maze import render, path_to_coords
from parse_config import parse_config, dict_validation
from maze_generator import MazeGenerator
import sys
import os
from random import Random, randint


def write_output(generator: MazeGenerator, output_file: str) -> None:
    with open(output_file, "w") as f:
        f.write(generator.get_hex_string())
        f.write("\n")
        f.write(f"{generator.entry[0]},{generator.entry[1]}\n")
        f.write(f"{generator.exit[0]},{generator.exit[1]}\n")
        f.write(f'{"".join(generator.solve())}\n')


def print_menu() -> None:
    print("\n\033[1;36m==== A-Maze-Ing ====\033[0m")
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
        perfect=validated_dict["PERFECT"],
    )
    seed = validated_dict.get("SEED", randint(1,1000))
    rng = Random(seed)
    generator.generate(rng)
    cells = generator.to_cells()
    path = generator.solve()
    coords = path_to_coords(path, generator.entry)
    render(cells, coords)
    print_menu()
    show_path = True
    colors = ["\033[1;96m", "\033[1;90m", "\033[1;91m", "\033[1;95m", "\033[1;94m"]
    color_idx = 0
    while True:
        key = readchar.readkey()
        if key == 'r':
            os.system("clear")
            seed += 1
            rng = Random(seed)
            generator.generate(rng)
            cells = generator.to_cells()
            path = generator.solve()
            coords = path_to_coords(path, generator.entry)
            if show_path is True:
                render(cells, coords)
                print_menu()
            else:
                render(cells)
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
            write_output(generator, validated_dict["OUTPUT_FILE"])
            print()
            sys.exit()


if __name__ == "__main__":
    main()
