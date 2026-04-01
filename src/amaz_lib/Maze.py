from dataclasses import dataclass
from numpy.typing import NDArray
from typing import Optional, Any


@dataclass
class Maze:
    """Represent a maze as a two-dimensional array of cells."""

    maze: Optional[NDArray[Any]] = None

    def get_maze(self) -> Optional[NDArray[Any]]:
        """Return the underlying maze array.

        Returns:
            The two-dimensional array representing the maze, or ``None`` if no
            maze has been set.
        """
        return self.maze

    def set_maze(self, new_maze: NDArray[Any]) -> None:
        """Set the maze array.

        Args:
            new_maze: A two-dimensional array containing the maze cells.
        """
        self.maze = new_maze

    def __str__(self) -> str:
        """Return a string representation of the maze.

        Each cell is converted to its string representation and concatenated
        line by line.

        Returns:
            A multiline string representation of the maze, or ``"None"`` if the
            maze is not set.
        """
        if self.maze is None:
            return "None"
        res = ""
        for line in self.maze:
            for cell in line:
                res += cell.__str__()
            res += "\n"
        return res

    def ascii_print(self) -> None:
        """Print an ASCII representation of the maze.

        The maze is rendered using underscores and vertical bars to show the
        walls of each cell. If no maze is set, ``"None"`` is printed.
        """
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
