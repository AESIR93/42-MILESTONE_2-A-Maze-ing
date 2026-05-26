def parse_config(filepath: str) -> dict:
	"""Parse the maze configuration file.

    Args:
        filepath: Path to the configuration file.

    Returns:
        A dictionary with the parsed and validated configuration.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If a required key is missing or has an invalid value.
    """
	validated_dict: {}
	with open(filepath, "r") as f:
		for line in f:
			if line.startswith("#") or line == "\n" :
				continue
			elif:
				if "=" not in line:
					raise SyntaxError("Bad syntax")
				else:
					line.split("=")
