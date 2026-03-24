from dataclasses import dataclass

import numpy
from .Cell import Cell
from .MazeGenerator import MazeGenerator


@dataclass
class Maze:
    maze: numpy.ndarray

    def get_maze(self) -> numpy.ndarray | None:
        return self.maze

    def set_maze(self, new_maze: numpy.ndarray) -> None:
        self.maze = new_maze

    def __str__(self) -> str:
        if self.maze is None:
            return "None"
        res = ""
        for line in self.maze:
            for cell in line:
                res += cell.__str__()
            res += "\n"
        return res

    def ascii_print(self) -> None:
        for cell in self.maze[0]:
            print("_", end="")
            if cell.get_north():
                print("__", end="")
            else:
                print("  ", end="")
        print("_")
        for line in self.maze:
            for cell in line:
                if cell is line[0] and cell.get_west():
                    print("|", end="")
                if cell.get_south() is True:
                    print("__", end="")
                else:
                    print("  ", end="")
                if cell.get_est() is True:
                    print("|", end="")
                else:
                    print("_", end="")
            print()
