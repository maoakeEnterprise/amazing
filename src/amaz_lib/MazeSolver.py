from abc import ABC, abstractmethod
from .Maze import Maze
import numpy as np


class MazeSolver(ABC):
    def __init__(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        self.start = (start[0] - 1, start[1] - 1)
        self.end = (end[0] - 1, end[1] - 1)

    @abstractmethod
    def solve(self, maze: Maze) -> str: ...


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
        self, maze: np.ndarray, actual: tuple[int, int]
    ) -> dict[str, int | None]:
        print(actual)
        path = {
            "N": (
                self.f((actual[1] - 1, actual[0]))
                if not maze[actual[1]][actual[0]].get_north() and actual[0] > 0
                else None
            ),
            "E": (
                self.f((actual[1], actual[0] + 1))
                if not maze[actual[1]][actual[0]].get_est()
                and actual[1] < len(maze) - 1
                else None
            ),
            "S": (
                self.f((actual[1] + 1, actual[0]))
                if not maze[actual[1]][actual[0]].get_south()
                and actual[0] < len(maze) - 1
                else None
            ),
            "W": (
                self.f((actual[1], actual[0] - 1))
                if not maze[actual[1]][actual[0]].get_west() and actual[1] > 0
                else None
            ),
        }
        return {
            k: v for k, v in sorted(path.items(), key=lambda item: item[0])
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
        actual = self.start
        path = ""

        return None

    def solve(self, maze: Maze) -> str:
        print(maze)
        res = self.get_path(self.start, maze.get_maze(), None)
        if res is None:
            raise Exception("Path not found")
        return res
