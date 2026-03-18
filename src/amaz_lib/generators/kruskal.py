from typing import Generator
import numpy as np
from ..classes.Cell import Cell
import math


def walls_to_maze(
    walls: list[tuple[int, int]],
    height: int,
    width: int,
) -> np.ndarray:
    maze: np.ndarray = np.array(
        [[Cell(value=0) for _ in range(width)] for _ in range(height)]
    )
    for wall in walls:
        x, y = wall
        match y - x:
            case 1:
                maze[math.trunc((x / width))][x % width].set_est(True)
                maze[math.trunc((y / width))][y % width].set_west(True)
            case 5:
                maze[math.trunc((x / width))][x % width].set_south(True)
                maze[math.trunc((y / width))][y % width].set_north(True)
    return maze


def is_in_same_set(sets: list[list[int]], wall: tuple[int, int]) -> bool:
    a, b = wall
    for set in sets:
        if a in set and b in set:
            return True
        if a in set or b in set:
            return False
    return False


def merge_sets(sets: list[list[int]], wall: tuple[int, int]) -> None:
    a, b = wall
    base_set = None
    for set in sets:
        if base_set is None and (a in set or b in set):
            base_set = set
        elif base_set and (a in set or b in set):
            base_set += set
            sets.remove(set)


def kraskal(
    height: int, width: int
) -> Generator[np.ndarray, None, np.ndarray]:
    sets = [[i] for i in range(height * width)]
    walls = []
    for h in range(height):
        for w in range(width - 1):
            walls += [(w + (width * h), w + (width * h) + 1)]
    for w in range(width):
        for h in range(height - 1):
            walls += [(w + (width * h), w + (width * h) + width)]
    np.random.shuffle(walls)

    yield walls_to_maze(walls, height, width)
    for wall in walls:
        if not is_in_same_set(sets, wall):
            merge_sets(sets, wall)
            walls.remove(wall)
            yield walls_to_maze(walls, height, width)
    return walls_to_maze(walls, height, width)


def main():
    try:
        for alg in kraskal(10, 10):
            maze = alg
            # print(maze)
            # print()
        print(maze)

    except GeneratorExit as maze:
        print(maze)


if __name__ == "__main__":
    main()
