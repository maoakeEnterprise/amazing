install:
	uv sync

run:
	uv run python3 a_maze_ing.py config.txt

debug:
	uv pdb python3 a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ .mypy_cache

lint:
	uv run python3 -m flake8 .
	uv run python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run python3 -m flake8 .
	uv run python3 -m mypy . --strict
