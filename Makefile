install:
	uv sync

run: install
	uv run python3 a_maze_ing.py config.txt

debug:
	uv pdb python3 a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ .mypy_cache .venv

lint:
	uv run flake8 . --exclude=.venv
	uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 .
	uv run mypy . --strict

run_test_parsing:
	PYTHONPATH=src uv run pytest tests/test_parsing.py

run_test_dfs:
	PYTHONPATH=src uv run pytest tests/test_Depth.py

run_test_maze_gen:
	PYTHONPATH=src uv run pytest tests/test_MazeGenerator.py
run_test:
	uv run pytest
