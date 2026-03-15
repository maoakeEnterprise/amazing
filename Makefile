install:
	pip install -r requirement.txt

run:
	python3 a_maze_ing.py config.txt

debug:
	pdb python3 a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ .mypy_cache

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
