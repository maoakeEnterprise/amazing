from abc import ABC, abstractmethod
from .Maze import Maze
import numpy as np


class MazeSolver(ABC):
    def __init__(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        self.start = (start[1] - 1, start[0] - 1)
        self.end = (end[1] - 1, end[0] - 1)

    @abstractmethod
    def solve(self, maze: Maze, height: int = None,
              width: int = None) -> str: ...


class AStar(MazeSolver):

    def __init__(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        super().__init__(start, end)

    def f(self, n):
        def g(n: tuple[int, int]) -> int:
            res = 0
            if n[0] < self.start[0]:
                res += self.start[0] - n[0]
            else:
                res += n[0] - self.start[0]
            if n[1] < self.start[1]:
                res += self.start[1] - n[1]
            else:
                res += n[1] - self.start[1]
            return res

        def h(n: tuple[int, int]) -> int:
            res = 0
            if n[0] < self.end[0]:
                res += self.end[0] - n[0]
            else:
                res += n[0] - self.end[0]
            if n[1] < self.end[1]:
                res += self.end[1] - n[1]
            else:
                res += n[1] - self.end[1]
            return res

        try:
            return g(n) + h(n)
        except Exception:
            return 1000

    def best_path(
        self,
        maze: np.ndarray,
        actual: tuple[int, int],
        last: str | None,
    ) -> dict[str, int]:
        path = {
            "N": (
                self.f((actual[0], actual[1] - 1))
                if not maze[actual[1]][actual[0]].get_north() and actual[1] > 0
                else None
            ),
            "E": (
                self.f((actual[0] + 1, actual[1]))
                if not maze[actual[1]][actual[0]].get_est()
                and actual[0] < len(maze[0]) - 1
                else None
            ),
            "S": (
                self.f((actual[0], actual[1] + 1))
                if not maze[actual[1]][actual[0]].get_south()
                and actual[1] < len(maze) - 1
                else None
            ),
            "W": (
                self.f((actual[0] - 1, actual[1]))
                if not maze[actual[1]][actual[0]].get_west() and actual[0] > 0
                else None
            ),
        }
        return {
            k: v
            for k, v in sorted(path.items(), key=lambda item: item[0])
            if v is not None and k != last
        }

    def get_opposit(self, dir: str) -> str:
        match dir:
            case "N":
                return "S"
            case "E":
                return "W"
            case "S":
                return "N"
            case "W":
                return "E"
            case _:
                return ""

    def get_next_pos(
        self, dir: str, actual: tuple[int, int]
    ) -> tuple[int, int]:
        match dir:
            case "N":
                return (actual[0], actual[1] - 1)
            case "E":
                return (actual[0] + 1, actual[1])
            case "S":
                return (actual[0], actual[1] + 1)
            case "W":
                return (actual[0] - 1, actual[1])
            case _:
                return actual

    def get_path(self, maze: np.ndarray) -> str | None:
        path = [(self.start, self.best_path(maze, self.start, None))]
        visited = [self.start]
        while len(path) > 0 and path[-1][0] != self.end:
            if len(path[-1][1]) == 0:
                path.pop(-1)
                if len(path) == 0:
                    break
                k = next(iter(path[-1][1]))
                path[-1][1].pop(k)
                continue

            while len(path[-1][1]) > 0:
                next_pos = self.get_next_pos(
                    list(path[-1][1].keys())[0], path[-1][0]
                )
                if next_pos in visited:
                    k = next(iter(path[-1][1]))
                    path[-1][1].pop(k)
                else:
                    break
            if len(path[-1][1]) == 0:
                path.pop(-1)
                continue

            pre = self.get_opposit(list(path[-1][1].keys())[0])
            path.append(
                (
                    next_pos,
                    self.best_path(maze, next_pos, pre),
                )
            )
            visited += [next_pos]
        if len(path) == 0:
            return None
        path[-1] = (self.end, {})
        return "".join(
            str(list(c[1].keys())[0]) for c in path if len(c[1]) > 0
        )

    def solve(self, maze: Maze) -> str:
        res = self.get_path(maze.get_maze())
        if res is None:
            raise Exception("Path not found")
        return res


class DepthFirstSearchSolver(MazeSolver):
    def __init__(self, start, end):
        self.start = (start[1] - 1, start[0] - 1)
        self.end = (end[1] - 1, end[0] - 1)

    def solve(self, maze: Maze, height: int = None,
              width: int = None) -> str:
        path_str = ""
        visited = np.zeros((height, width), dtype=bool)
        path = list()
        move = list()
        maze_s = maze.get_maze()
        coord = self.start
        h_w = (height, width)
        while coord != self.end:
            visited[coord] = True
            path.append(coord)
            rand_p = self.random_path(visited, coord, maze_s, h_w)

            if not rand_p:
                path, move = self.back_on_step(path, visited, maze_s, h_w,
                                               move)
                if not path:
                    break
                coord = path[-1]
                rand_p = self.random_path(visited, coord, maze_s, h_w)
            next = self.next_path(rand_p)
            move.append(next)
            coord = self.next_cell(coord, next)
        for m in move:
            path_str += m
        if not path:
            raise Exception("Path not found")
        return path_str

    @staticmethod
    def random_path(visited: np.ndarray, coord: tuple,
                    maze: np.ndarray, h_w: tuple) -> list:
        random_p = []
        h, w = h_w
        y, x = coord

        if y - 1 >= 0 and not maze[y][x].get_north() and not visited[y - 1][x]:
            random_p.append("N")

        if y + 1 < h and not maze[y][x].get_south() and not visited[y + 1][x]:
            random_p.append("S")

        if x - 1 >= 0 and not maze[y][x].get_west() and not visited[y][x - 1]:
            random_p.append("W")

        if x + 1 < w and not maze[y][x].get_est() and not visited[y][x + 1]:
            random_p.append("E")
        return random_p

    @staticmethod
    def next_path(rand_path: list) -> str:
        return np.random.choice(rand_path)

    @staticmethod
    def back_on_step(path: list, visited: np.ndarray,
                     maze: np.ndarray, h_w: tuple, move: list) -> list:
        while path:
            last = path[-1]
            if DepthFirstSearchSolver.random_path(visited, last, maze, h_w):
                break
            path.pop()
            move.pop()
        return path, move

    @staticmethod
    def next_cell(coord: tuple, next: str) -> tuple:
        y, x = coord
        next_step = {"N": (-1, 0), "S": (1, 0), "W": (0, -1), "E": (0, 1)}
        add_y, add_x = next_step[next]
        return (y + add_y, x + add_x)
