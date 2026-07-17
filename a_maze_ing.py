#!/usr/bin/env python3

import readchar
from Amazeing.print_maze import render, path_to_coords, render_path
from Amazeing.parse_config import parse_config, dict_validation
from mazegen.maze_generator import MazeGenerator
import sys
from typing import Optional
import os
import io
from random import Random, randint


def write_output(generator: MazeGenerator, output_file: str) -> None:
    with open(output_file, "w") as f:
        f.write(generator.get_hex_string())
        f.write("\n")
        f.write(f"{generator.entry[0]},{generator.entry[1]}\n")
        f.write(f"{generator.exit[0]},{generator.exit[1]}\n")
        f.write(f'{"".join(generator.solve())}\n')


def print_menu(warning: Optional[str]) -> None:
    print("\n\033[4;1;92m==== A-Maze-Ing ====\033[0m")
    if warning:
        print(f"\n\033[1;2;3;93m~ {warning} ~\033[0m")
    print("\n\033[97mChoose an option to interact with your maze!")
    print("\nOptions:")
    print("     r: Regenerate maze")
    print("     p: Show/hide path")
    print("     c: Change color")
    print("     q: quit\n")
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
    seed = validated_dict.get("SEED", randint(1, 1000))
    rng = Random(seed)
    stderr_backup = sys.stderr
    sys.stderr = io.StringIO()
    generator.generate(rng)
    warning = sys.stderr.getvalue().strip()
    sys.stderr = stderr_backup
    cells = generator.to_cells()
    path = generator.solve()
    coords = path_to_coords(path, generator.entry)
    render(cells, coords)
    if warning:
        print_menu(warning)
    else:
        print_menu(None)
    show_path = False
    colors = ["\033[1;95m", "\033[1;90m",
              "\033[1;91m", "\033[1;96m",
              "\033[1;94m"]
    color_idx = 0
    while True:
        key = readchar.readkey()
        if key == 'r':
            os.system("clear")
            seed += 1
            rng = Random(seed)
            stderr_backup = sys.stderr
            sys.stderr = io.StringIO()
            generator.generate(rng)
            warning = sys.stderr.getvalue().strip()
            sys.stderr = stderr_backup
            cells = generator.to_cells()
            path = generator.solve()
            coords = path_to_coords(path, generator.entry)
            if show_path is True:
                render(cells, coords, colors[color_idx])
                render_path(coords)
                maze_final = len(cells) * 2 + 1
                print(f"\033[{maze_final + 1};1H", end="")
                if warning:
                    print_menu(warning)
                else:
                    print_menu(None)
            else:
                render(cells, coords, colors[color_idx])
                if warning:
                    print_menu(warning)
                else:
                    print_menu(None)
        elif key == 'p':
            os.system("clear")
            if show_path is True:
                show_path = False
                render(cells, coords, colors[color_idx])
                if warning:
                    print_menu(warning)
                else:
                    print_menu(None)
            elif show_path is False:
                show_path = True
                render(cells, coords, colors[color_idx])
                render_path(coords)
                maze_final = len(cells) * 2 + 1
                print(f"\033[{maze_final + 1};1H", end="")
                if warning:
                    print_menu(warning)
                else:
                    print_menu(None)
        elif key == 'c':
            os.system("clear")
            color_idx = (color_idx + 1) % len(colors)
            if show_path is True:
                render(cells, coords, colors[color_idx])
                render_path(coords, False)
                maze_final = len(cells) * 2 + 1
                print(f"\033[{maze_final + 1};1H", end="")
                if warning:
                    print_menu(warning)
                else:
                    print_menu(None)
            elif show_path is False:
                render(cells, coords, colors[color_idx])
                if warning:
                    print_menu(warning)
                else:
                    print_menu(None)
        elif key == 'q':
            write_output(generator, validated_dict["OUTPUT_FILE"])
            print()
            sys.exit()


if __name__ == "__main__":
    main()
