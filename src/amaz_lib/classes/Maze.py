from dataclasses import dataclass
from .Cell import Cell


@dataclass
class Maze:
    maze: list[list[Cell]]

    def get_maze(self) -> list[list[Cell]] | None:
        return self.maze

    def set_maze(self, new_maze: list[list[Cell]]) -> None:
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

    def export_maze(self, file_name: str):
        with open(file_name, "w") as file:
            file.write(self.__str__())
