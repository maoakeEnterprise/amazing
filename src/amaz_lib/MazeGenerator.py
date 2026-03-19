from abc import ABC, abstractmethod
from typing import Generator
import numpy as np
from .Cell import Cell
import math


class MazeGenerator(ABC):
    @abstractmethod
    def generator(
        self, height: int, width: int
    ) -> Generator[np.ndarray, None, np.ndarray]: ...


class Kruskal(MazeGenerator):
    @staticmethod
    def walls_to_maze(
        walls: list[tuple[int, int]], height: int, width: int
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
                case width:
                    maze[math.trunc((x / width))][x % width].set_south(True)
                    maze[math.trunc((y / width))][y % width].set_north(True)
        for x in range(height):
            for y in range(width):
                if x == 0:
                    maze[x][y].set_north(True)
                if x == height - 1:
                    maze[x][y].set_south(True)
                if y == 0:
                    maze[x][y].set_est(True)
                if y == width - 1:
                    maze[x][y].set_west(True)
        return maze

    @staticmethod
    def is_in_same_set(sets: list[list[int]], wall: tuple[int, int]) -> bool:
        a, b = wall
        for set in sets:
            if a in set and b in set:
                return True
            if a in set or b in set:
                return False
        return False

    @staticmethod
    def merge_sets(sets: list[list[int]], wall: tuple[int, int]) -> None:
        a, b = wall
        base_set = None
        for set in sets:
            if base_set is None and (a in set or b in set):
                base_set = set
            elif base_set and (a in set or b in set):
                base_set += set
                sets.remove(set)

    def generator(
        self, height: int, width: int
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

        yield self.walls_to_maze(walls, height, width)
        for wall in walls:
            if not self.is_in_same_set(sets, wall):
                self.merge_sets(sets, wall)
                walls.remove(wall)
                yield self.walls_to_maze(walls, height, width)
        return self.walls_to_maze(walls, height, width)


def main():
    try:
        for alg in MazeGenerator.Kruskal.kruskal(10, 10):
            maze = alg
            # print(maze)
            # print()
        print(maze)

    except GeneratorExit as maze:
        print(maze)


if __name__ == "__main__":
    main()
