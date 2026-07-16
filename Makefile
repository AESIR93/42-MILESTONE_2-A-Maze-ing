install:
	@pip install -r requirements.txt
	@pip install mazegen-1.0.0-py3-none-any.whl
run:
	-@python3 a_maze_ing.py config.txt
	-@$(MAKE) --no-print-directory clean
debug:
	@python3 -m pdb a_maze_ing.py config.txt
clean:
	@rm -rf __pycache__ .mypy_cache */__pycache__ 
lint:
	@flake8 .
	@mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs