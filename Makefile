install:
	pip install -r requirements.txt
run:
	clear
	@$(MAKE) install
	-@python3 a_maze_ing.py config.txt
	@$(MAKE) clean
debug:
	python3 -m pdb a_maze_ing.py config.txt
clean:
	rm -rf __pycache__ .mypy_cache
lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs