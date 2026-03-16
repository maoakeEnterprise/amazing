from typing import Generator
import numpy as np
from .. import Cell


def kraskal(
    height: int, width: int
) -> Generator[np.ndarray, None, np.ndarray]:
    maze = np.array([[Cell(value=15) for _ in range(height)] * width])
    cells_checked = np.array([[False for _ in range(height)] * width])
    excepted_end = np.array([[True for _ in range(height)] * width])

    while cells_checked != excepted_end:
        yield maze
    return maze
