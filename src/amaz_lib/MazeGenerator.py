from abc import ABC, abstractmethod
from typing import Generator, Set
import numpy as np
from .Cell import Cell
import math


class MazeGenerator(ABC):
    @abstractmethod
    def generator(
        self, height: int, width: int, seed: int | None = None
    ) -> Generator[np.ndarray, None, np.ndarray]: ...

    @staticmethod
    def get_cell_ft(width: int, height: int) -> set:
        forty_two = set()
        y, x = (int(height / 2), int(width / 2))
        forty_two.add((y, x - 1))
        forty_two.add((y, x - 2))
        forty_two.add((y, x - 3))
        forty_two.add((y - 1, x - 3))
        forty_two.add((y - 2, x - 3))
        forty_two.add((y + 1, x - 1))
        forty_two.add((y + 2, x - 1))
        forty_two.add((y, x + 1))
        forty_two.add((y, x + 2))
        forty_two.add((y, x + 3))
        forty_two.add((y - 1, x + 3))
        forty_two.add((y - 2, x + 3))
        forty_two.add((y - 2, x + 2))
        forty_two.add((y - 2, x + 1))
        forty_two.add((y + 1, x + 1))
        forty_two.add((y + 2, x + 1))
        forty_two.add((y + 2, x + 2))
        forty_two.add((y + 2, x + 3))
        return forty_two


class Kruskal(MazeGenerator):
    class Set:
        def __init__(self, cells: list[int]) -> None:
            self.cells: list[int] = cells

    class Sets:
        def __init__(self, sets: list[Set]) -> None:
            self.sets = sets

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
    def is_in_same_set(sets: Sets, wall: tuple[int, int]) -> bool:
        a, b = wall
        for set in sets.sets:
            if a in set.cells and b in set.cells:
                return True
            elif a in set.cells or b in set.cells:
                return False
        return False

    @staticmethod
    def merge_sets(sets: Sets, wall: tuple[int, int]) -> None:
        a, b = wall
        base_set = None
        for i in range(len(sets.sets)):
            if base_set is None and (
                a in sets.sets[i].cells or b in sets.sets[i].cells
            ):
                base_set = sets.sets[i]
            elif base_set and (
                a in sets.sets[i].cells or b in sets.sets[i].cells
            ):
                base_set.cells += sets.sets[i].cells
                sets.sets.pop(i)
                return
        raise Exception("two sets not found")

    @staticmethod
    def touch_ft(
        width: int,
        wall: tuple[int, int],
        cells_ft: None | set[tuple[int, int]],
    ) -> bool:
        if cells_ft is None:
            return False
        s1 = (math.trunc(wall[0] / width), wall[0] % width)
        s2 = (math.trunc(wall[1] / width), wall[1] % width)
        return s1 in cells_ft or s2 in cells_ft

    def generator(
        self, height: int, width: int, seed: int | None = None
    ) -> Generator[np.ndarray, None, np.ndarray]:
        cells_ft = None
        if height > 10 and width > 10:
            cells_ft = self.get_cell_ft(width, height)

        if seed is not None:
            np.random.seed(seed)
        sets = self.Sets([self.Set([i]) for i in range(height * width)])
        walls = []
        for h in range(height):
            for w in range(width - 1):
                walls += [(w + (width * h), w + (width * h) + 1)]
        for h in range(height - 1):
            for w in range(width):
                walls += [(w + (width * h), w + (width * (h + 1)))]
        np.random.shuffle(walls)

        yield self.walls_to_maze(walls, height, width)
        while (len(sets.sets) != 1 and cells_ft is None) or (
            len(sets.sets) != 19 and cells_ft is not None
        ):
            for wall in walls:
                if not self.is_in_same_set(sets, wall) and not self.touch_ft(
                    width, wall, cells_ft
                ):
                    self.merge_sets(sets, wall)
                    walls.remove(wall)
                    yield self.walls_to_maze(walls, height, width)
                if (len(sets.sets) == 1 and cells_ft is None) or (
                    len(sets.sets) == 19 and cells_ft is not None
                ):
                    break
        return self.walls_to_maze(walls, height, width)


class DepthFirstSearch(MazeGenerator):

    def generator(
        self, height: int, width: int, seed: int = None
    ) -> Generator[np.ndarray, None, np.ndarray]:
        if seed is not None:
            np.random.seed(seed)
        maze = self.init_maze(width, height)
        forty_two = self.get_cell_ft(width, height)
        visited = np.zeros((height, width), dtype=bool)
        visited = self.lock_cell_ft(visited, forty_two)
        path = list()
        w_h = (width, height)
        coord = (0, 0)
        x, y = coord
        first_iteration = True

        while path or first_iteration:
            first_iteration = False

            visited[y, x] = True
            path = self.add_cell_visited(coord, path)

            random_c = self.random_cells(visited, coord, w_h)

            if not random_c:
                path = self.back_on_step(path, w_h, visited)
                if not path:
                    break
                coord = path[-1]
                random_c = self.random_cells(visited, coord, w_h)
                x, y = coord

            wall = self.next_step(random_c)
            maze[y][x] = self.broken_wall(maze[y][x], wall)

            coord = self.next_cell(x, y, wall)
            wall_r = self.reverse_path(wall)
            x, y = coord
            maze[y][x] = self.broken_wall(maze[y][x], wall_r)
            yield maze
        return maze

    @staticmethod
    def init_maze(width: int, height: int) -> np.ndarray:
        maze = np.array(
            [[Cell(value=15) for _ in range(width)] for _ in range(height)]
        )
        return maze

    @staticmethod
    def add_cell_visited(coord: tuple, path: set) -> list:
        path.append(coord)
        return path

    @staticmethod
    def random_cells(visited: np.array, coord: tuple, w_h: tuple) -> list:
        rand_cell = []
        x, y = coord
        width, height = w_h

        if y - 1 >= 0 and not visited[y - 1][x]:
            rand_cell.append("N")

        if y + 1 < height and not visited[y + 1][x]:
            rand_cell.append("S")

        if x - 1 >= 0 and not visited[y][x - 1]:
            rand_cell.append("W")

        if x + 1 < width and not visited[y][x + 1]:
            rand_cell.append("E")
        return rand_cell

    @staticmethod
    def next_step(rand_cell: list) -> str:
        return np.random.choice(rand_cell)

    @staticmethod
    def broken_wall(cell: Cell, wall: str) -> Cell:
        if wall == "N":
            cell.set_north(False)
        elif wall == "S":
            cell.set_south(False)
        elif wall == "W":
            cell.set_west(False)
        elif wall == "E":
            cell.set_est(False)
        return cell

    @staticmethod
    def next_cell(x: int, y: int, next: str) -> tuple:
        next_step = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "E": (1, 0)}
        add_x, add_y = next_step[next]
        return (x + add_x, y + add_y)

    @staticmethod
    def reverse_path(direction: str) -> str:
        return {"N": "S", "S": "N", "W": "E", "E": "W"}[direction]

    @staticmethod
    def back_on_step(path: list, w_h: tuple, visited: np.array) -> list:
        while path:
            last = path[-1]
            if DepthFirstSearch.random_cells(visited, last, w_h):
                break
            path.pop()
        return path

    @staticmethod
    def lock_cell_ft(
        visited: np.ndarray, forty_two: set[tuple[int]]
    ) -> np.ndarray:
        tab = [cell for cell in forty_two]
        for cell in tab:
            visited[cell] = True
        return visited
