from dataclasses import dataclass
from numpy.typing import NDArray
from typing import Optional, Any


@dataclass
class Maze:
    maze: Optional[NDArray[Any]] = None

    def get_maze(self) -> Optional[NDArray[Any]]:
        return self.maze

    def set_maze(self, new_maze: NDArray[Any]) -> None:
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
        if self.maze is None:
            print("None")
            return
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
