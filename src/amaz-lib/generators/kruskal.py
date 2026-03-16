from typing import Generator
import numpy as np
from .. import Cell


def kraskal(height: int, width: int) -> Generator[None, None, None]:
    maze = np.array([[Cell(value=15) for _ in range(height)] * width])
