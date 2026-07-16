#!/usr/bin/env python3

import sys
from typing import Any
import os


def parse_config(filepath: str) -> dict[str, str]:
    """Parse the maze configuration file.

    Args:
        filepath: Path to the configuration file.

    Returns:
        A dictionary with the parsed and validated configuration.

    Raises:
        FileNotFoundError: If the file does not exist.
        SyntaxError: If the syntax is not KEY=VALUE.
    """
    config = {}
    try:
        with open(filepath, "r") as f:
            for line in f:
                try:
                    if line.startswith("#") or line == "\n":
                        continue
                    else:
                        if "=" not in line:
                            raise SyntaxError("Bad syntax")
                        else:
                            key, value = line.split("=", 1)
                            key = key.strip()
                            value = value.strip()
                            config[key] = value
                except SyntaxError as e:
                    print(e)
                    sys.exit(1)
    except FileNotFoundError as er:
        print(er)
        sys.exit(1)
    return config


def dict_validation(config: dict[str, str]) -> dict[str, Any]:
    """Validate the dictionary elements from parse_config.

    Args:
        config: Already parsed dictionary.

    Returns:
        A dictionary ready for the generator to use.

    Raises:
        ValueError: If a required key is missing or has an invalid value.
    """
    if config is None:
        sys.exit(1)
    required_keys = ["WIDTH", "HEIGHT", "ENTRY",
                     "EXIT", "OUTPUT_FILE", "PERFECT"]
    valid_keys = ["WIDTH", "HEIGHT", "ENTRY",
                  "EXIT", "OUTPUT_FILE", "PERFECT", "SEED"]
    try:
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Required parameter missing: {key}")
        for valid in config.keys():
            if valid not in valid_keys:
                raise ValueError(f"Key not valid: {valid}")
    except ValueError as e:
        print(e)
        sys.exit(1)
    final_dict: dict[str, Any] = {}
    try:
        for key, value in config.items():
            if key in ("WIDTH", "HEIGHT"):
                try:
                    int_value = int(value)
                except ValueError:
                    print("WIDTH and HEIGHT must be integers")
                    sys.exit(1)
                if int_value >= 0:
                    final_dict[key] = int_value
                else:
                    raise ValueError("WIDTH and HEIGHT can't be negative")
            if key in ("ENTRY", "EXIT"):
                try:
                    x, y = value.split(",")
                    x, y = x.strip(), y.strip()
                    int_x, int_y = int(x), int(y)
                except ValueError:
                    print("For ENTRY and EXIT you must enter 2 int values")
                    sys.exit(1)
                if int_x >= 0 and int_y >= 0:
                    final_dict[key] = (int_x, int_y)
                else:
                    raise ValueError("Coordinates can't be negative")
            if key == "OUTPUT_FILE":
                if value == "":
                    raise ValueError(
                        "You need to specify a name for the output file!")
                elif not value.endswith(".txt") or value == "requirements.txt" or value == "config.txt":
                    raise ValueError(
                        "OUTPUT_FILE must end in .txt, and can`t override requirements or config itself")
                else:
                    final_dict[key] = value
            if key == "PERFECT":
                if value not in ("True", "False"):
                    raise ValueError(
                        "PERFECT parameter only accepts True or False")
                else:
                    final_dict[key] = value == "True"
            if key == "SEED":
                try:
                    final_dict[key] = int(value)
                except ValueError:
                    print("SEED parameter only accepts integers")
                    sys.exit(1)
        if final_dict["ENTRY"] == final_dict["EXIT"]:
            raise ValueError("ENTRY and EXIT can't be the same cell u genius")
        if (final_dict["ENTRY"][0] >= final_dict["WIDTH"]
                or final_dict["ENTRY"][1] >= final_dict["HEIGHT"]):
            raise ValueError(
                "ENTRY coordinates must be within maze limits u idiot")
        if (final_dict["EXIT"][0] >= final_dict["WIDTH"]
                or final_dict["EXIT"][1] >= final_dict["HEIGHT"]):
            raise ValueError(
                "EXIT coordinates must be within maze limits u dumbo")
        return final_dict
    except ValueError as e:
        print(e)
        sys.exit(1)
