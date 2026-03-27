from typing import Generator
from typing_extensions import Self
from pydantic import BaseModel, Field, model_validator, ConfigDict

from src.amaz_lib import Maze, MazeGenerator, MazeSolver


class AMazeIng(BaseModel):
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

    @model_validator(mode="after")
    def check_entry_exit(self) -> Self:
        if self.entry[0] > self.width or self.entry[1] > self.height:
            raise ValueError("Entry coordinates exceed the maze size")
        if self.exit[0] > self.width or self.exit[1] > self.height:
            raise ValueError("Exit coordinates exceed the maze size")
        return self

    def generate(self) -> Generator[Maze, None, None]:
        for array in self.generator.generator(self.height, self.width):
            self.maze.set_maze(array)
            yield self.maze
        return

    def solve_path(self) -> str:
        return self.solver.solve(self.maze, self.height, self.width)

    def __str__(self) -> str:
        res = self.maze.__str__()
        res += "\n"
        res += f"{self.entry[0]},{self.entry[1]}\n"
        res += f"{self.exit[0]},{self.exit[1]}\n"
        res += self.solve_path()
        res += "\n"
        return res
