from typing import Generator
from typing_extensions import Self
from pydantic import BaseModel, Field, model_validator, ConfigDict

from mazegen import Maze, MazeGenerator, MazeSolver


class AMazeIng(BaseModel):
    """Represent a complete maze configuration, generation,
    and solving setup.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    width: int = Field(ge=4)
    height: int = Field(ge=4)
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str = Field(min_length=3)
    perfect: bool = Field(default=True)
    maze: Maze = Field(default=Maze(None))
    generator: MazeGenerator
    solver: MazeSolver
    seed: int | None = Field(default=None)

    @model_validator(mode="after")
    def check_entry_exit(self) -> Self:
        """Validate that entry and exit coordinates fit within maze bounds.

        Returns:
            The validated model instance.

        Raises:
            ValueError: If entry or exit coordinates exceed maze dimensions.
        """
        if self.entry[0] > self.width or self.entry[1] > self.height:
            raise ValueError("Entry coordinates exceed the maze size")
        if self.exit[0] > self.width or self.exit[1] > self.height:
            raise ValueError("Exit coordinates exceed the maze size")
        if self.entry == self.exit:
            raise ValueError("Entry and Exit coordinates cant be the same")
        if self.width <= 10 or self.height <= 10:
            print("Height or width to low for disply forty two logo")
        return self

    def generate(self) -> Generator[Maze, None, None]:
        """Generate the maze step by step.

        The internal maze state is updated at each generation step.

        Yields:
            The current maze state after each generation step.
        """
        for array in self.generator.generator(
            self.height, self.width, self.seed
        ):
            self.maze.set_maze(array)
            yield self.maze
        return

    def solve_path(self) -> str:
        """Solve the current maze and return the path string.

        Returns:
            A string of direction letters representing the solution path.
        """
        return self.solver.solve(self.maze, self.height, self.width)

    def __str__(self) -> str:
        """Return a string representation of the maze and its solution.

        The output includes the maze, entry coordinates, exit coordinates, and
        the computed solution path.

        Returns:
            A formatted string representation of the maze data.
        """
        res = self.maze.__str__()
        res += "\n"
        res += f"{self.entry[0]},{self.entry[1]}\n"
        res += f"{self.exit[0]},{self.exit[1]}\n"
        res += self.solve_path()
        res += "\n"
        return res
