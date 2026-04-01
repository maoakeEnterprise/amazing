build:
	uv build --clear --wheel
	cp dist/*.whl mazegen-1.0.0-py3-none-any.whl

install:
	uv sync
	uv pip install mlx-2.2-py3-none-any.whl

run: install
	uv run python3 a_maze_ing.py config.txt

run_windows:
	.venv\Scripts\python -m a_maze_ing config.txt

debug:
	uv pdb python3 a_maze_ing.py config.txt

clean:
	rm -rf */**/__pycache__ */__pycache__ __pycache__ .mypy_cache .venv dist build */**/*.egg-info */*.egg-info *.egg-info test.txt

fclean: clean
	rm mazegen-1.0.0-py3-none-any.whl 

lint:
	uv run flake8 . --exclude=.venv
	uv run env PYTHONPATH=src python3 -m mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs src
	uv run env PYTHONPATH=src python3 -m mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs tests
	uv run env PYTHONPATH=src python3 -m mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs a_maze_ing.py

lint-strict:
	uv run flake8 . --exclude=.venv
	uv run env PYTHONPATH=src python3 -m mypy --strict src
	uv run env PYTHONPATH=src python3 -m mypy --strict tests
	uv run env PYTHONPATH=src python3 -m mypy --strict a_maze_ing.py

run_test_parsing:
	PYTHONPATH=src uv run pytest tests/test_parsing.py

run_test_dfs:
	PYTHONPATH=src uv run pytest tests/test_Depth.py

run_test_maze_gen:
	PYTHONPATH=src uv run pytest tests/test_MazeGenerator.py
run_test:
	uv run pytest
mlx:
	uv run python3 test.py

.PHONY: build install run debug clean fclean lint lint-strict run_test
