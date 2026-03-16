install:
	uv sync

run: install
	uv run python3 a_maze_ing.py config.txt

debug:
	uv pdb python3 a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ .mypy_cache .venv

lint:
	uv run flake8 .
	uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 .
	uv run mypy . --strict

run_test:
	PYTHONPATH=src uv run python3 test/test_parsing.py
