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


class DepthFirstSearch:

    @staticmethod
    def generator(width: int, height: int) -> np.ndarray:
        maze = DepthFirstSearch.init_maze(width, height)
        visited = np.zeros((height, width), dtype=bool)
        path = list()
        w_h = (width, height)
        coord = (0, 0)
        x, y = coord
        first = True

        while path or first:
            first = False
            visited[y, x] = True
            path = DepthFirstSearch.add_cell_visited(coord, path)
            random_c = DepthFirstSearch.random_cells(visited, coord, w_h)
            if len(random_c) == 0:
                path = DepthFirstSearch.back_on_step(path, w_h, visited)
                if path:
                    coord = path[-1]
                random_c = DepthFirstSearch.random_cells(visited, coord, w_h)
                x, y = coord
                if not path:
                    break

            wall = DepthFirstSearch.next_step(random_c)
            maze[y][x] = DepthFirstSearch.broken_wall(maze[y][x], wall)

            coord = DepthFirstSearch.next_cell(x, y, wall)
            wall_r = DepthFirstSearch.reverse_path(wall)
            x, y = coord
            maze[y][x] = DepthFirstSearch.broken_wall(maze[y][x], wall_r)
        return maze

    @staticmethod
    def init_maze(width: int, height: int) -> np.ndarray:
        maze = np.array([[Cell(value=15) for _ in range(width)]
                        for _ in range(height)])
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
        next_step = {
            "N": (0, -1),
            "S": (0, 1),
            "W": (-1, 0),
            "E": (1, 0)
        }
        add_x, add_y = next_step[next]
        return (x + add_x, y + add_y)

    @staticmethod
    def reverse_path(next: str) -> str:
        reverse = {
            "N": "S",
            "S": "N",
            "W": "E",
            "E": "W"
        }
        return reverse[next]

    @staticmethod
    def back_on_step(path: list, w_h: tuple, visited: np.array) -> list:
        last = path[-1]
        r_cells = DepthFirstSearch.random_cells(visited,  last, w_h)
        while len(path) > 0:
            path.pop()
            if path:
                last = path[-1]
            r_cells = DepthFirstSearch.random_cells(visited,  last, w_h)
            if r_cells:
                break
        return path
