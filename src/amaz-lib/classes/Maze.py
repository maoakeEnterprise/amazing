from sys import stdout
import numpy as np
from pydantic import BaseModel


class Maze(BaseModel):
    maze: np.ndarray

    def __str__(self) -> str:
        res = ""
        for _ in self.maze:
            for cell in self.maze:
                res += cell
            res += "\n"
        return res
