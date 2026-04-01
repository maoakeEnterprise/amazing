from mazegen import DepthFirstSearch
from mazegen import Cell
import numpy as np


class TestDepth:

    def test_init_maze(self) -> None:
        maze = DepthFirstSearch.init_maze(10, 10)
        cell = Cell(value=15)
        maze[1][1].set_est(False)
        assert maze[0][0].value == cell.value

    def test_rand_cells(self) -> None:
        w_h = (10, 10)
        lst = np.zeros((10, 10), dtype=bool)
        lst[0, 0] = True
        rand_cells = DepthFirstSearch.random_cells(lst, (0, 1), w_h)
        assert len(rand_cells) == 2

    def test_next_cell(self) -> None:
        coord = (5, 4)
        x, y = coord
        assert DepthFirstSearch.next_cell(x, y, "N") == (2, 3)

    def test_reverse_path(self) -> None:
        assert DepthFirstSearch.reverse_path("N") == "S"
