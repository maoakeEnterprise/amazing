from dataclasses import field
from os import eventfd_read
from typing import Generator
import numpy
from typing_extensions import Self
from pydantic import AfterValidator, BaseModel, Field, model_validator

from amaz_lib import Maze, MazeGenerator, MazeSolver
from amaz_lib.Cell import Cell


class AMazeIng(BaseModel):
    width: int = Field(ge=3)
    height: int = Field(ge=3)
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str = Field(min_length=3)
    perfect: bool = Field(default=True)
    maze: Maze = Field(default=Maze(maze=numpy.array([])))
    generator: MazeGenerator
    solver: MazeSolver

    @model_validator(mode="after")
    def check_entry_exit(self) -> Self:
        if self.entry[0] >= self.width or self.entry[1] >= self.height:
            raise ValueError("Entry coordinates exceed the maze size")
        if self.exit[0] >= self.width or self.exit[1] >= self.height:
            raise ValueError("Exit coordinates exceed the maze size")
        return self

    def generate(self) -> Generator[Maze, None, None]:
        for array in self.generator.generator(self.height, self.width):
            self.maze.set_maze(array)
            yield self.maze

    def solve_path(self) -> str:
        return self.solver.solve(self.maze)

    def __str__(self) -> str:
        res = self.maze.__str__()
        res += "\n"
        res += f"{self.entry[0]},{self.entry[1]}\n"
        res += f"{self.exit[0]},{self.exit[1]}\n"
        res += self.solve_path()
        res += "\n"
        return res
