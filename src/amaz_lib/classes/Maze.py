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

    def ascii_print(self) -> None:
        for line in self.maze:
            if line is self.maze[0]:
                for cell in line:
                    print("_", end="")
                    if cell.get_north():
                        print("__", end="")
                    else:
                        print("  ", end="")
                print()
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
