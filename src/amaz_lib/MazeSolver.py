from abc import ABC, abstractmethod
from .Maze import Maze


class MazeSolver(ABC):
    @abstractmethod
    def solve(self, maze: Maze) -> str: ...
