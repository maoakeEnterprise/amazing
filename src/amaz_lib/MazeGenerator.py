from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generator, Set
import numpy as np
from .Cell import Cell
import math


class MazeGenerator(ABC):
    @abstractmethod
    def generator(
        self, height: int, width: int
    ) -> Generator[np.ndarray, None, np.ndarray]: ...


class Kruskal(MazeGenerator):
    class Set:
        def __init__(self, cells: list[int]) -> None:
            self.cells: list[int] = cells

    @staticmethod
    def walls_to_maze(
        walls: np.ndarray, height: int, width: int
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
                    maze[x][y].set_west(True)
                if y == width - 1:
                    maze[x][y].set_est(True)
        return maze

    @staticmethod
    def is_in_same_set(sets: np.ndarray, wall: tuple[int, int]) -> bool:
        a, b = wall
        for set in sets:
            if a in set.cells and b in set.cells:
                return True
            elif a in set.cells or b in set.cells:
                return False
        return False

    @staticmethod
    def merge_sets(sets: np.ndarray, wall: tuple[int, int]) -> None:
        a, b = wall
        base_set = None
        for i in range(len(sets)):
            if base_set is None and (a in sets[i].cells or b in sets[i].cells):
                base_set = sets[i]
            elif base_set and (a in sets[i].cells or b in sets[i].cells):
                base_set.cells += sets[i].cells
                np.delete(sets, i)
                return
        raise Exception("two sets not found")

    def generator(
        self, height: int, width: int
    ) -> Generator[np.ndarray, None, np.ndarray]:
        sets = np.array([self.Set([i]) for i in range(height * width)])
        walls = []
        for h in range(height):
            for w in range(width - 1):
                walls += [(w + (width * h), w + (width * h) + 1)]
        for h in range(height - 1):
            for w in range(width):
                walls += [(w + (width * h), w + (width * (h + 1)))]
        print(walls)
        np.random.shuffle(walls)

        yield self.walls_to_maze(walls, height, width)
        for wall in walls:
            if not self.is_in_same_set(sets, wall):
                self.merge_sets(sets, wall)
                walls.remove(wall)
                yield self.walls_to_maze(walls, height, width)
        print(f"nb sets: {len(sets)}")
        return self.walls_to_maze(walls, height, width)
