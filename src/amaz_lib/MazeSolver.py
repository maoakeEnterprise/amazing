from abc import ABC, abstractmethod
from .Maze import Maze


class MazeSolver(ABC):
    @abstractmethod
    @classmethod
    def solve(cls, maze: Maze) -> str: ...
