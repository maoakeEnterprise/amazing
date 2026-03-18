from dataclasses import dataclass

import numpy
from .Cell import Cell


@dataclass
class Maze:
    maze: numpy.ndarray
    start: tuple[int, int]
    end: tuple[int, int]

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
        res += "\n"
        res += f"{self.start[0]},{self.start[1]}\n"
        res += f"{self.end[0]},{self.end[1]}\n"
        return res

    def export_maze(self, file_name: str) -> None:
        with open(file_name, "w") as file:
            file.write(self.__str__())

    def solver(self) -> str:
        pass
