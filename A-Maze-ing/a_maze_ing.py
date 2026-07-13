#!/usr/bin/env python3

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mazegen.maze_generator import MazeGenerator
from parse_config import parse_config, dict_validation
from print_maze import render


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
    render(cells)


if __name__=="__main__":
    main()

