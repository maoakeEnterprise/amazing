from amaz_lib.Cell import Cell
import numpy as np
from amaz_lib import AStar, Maze


def test_solver() -> None:
    maze = Maze(
        np.array(
            [
                [Cell(value=13), Cell(value=3), Cell(value=11)],
                [Cell(value=9), Cell(value=4), Cell(value=6)],
                [Cell(value=12), Cell(value=5), Cell(value=7)],
            ]
        )
    )
    print(maze)
    solver = AStar((1, 1), (3, 3))
    res = solver.solve(maze)
    assert res == "ESWSEE"
