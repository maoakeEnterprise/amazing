from amaz_lib.MazeGenerator import DepthFirstSearch
from amaz_lib.Cell import Cell


class TestDepth:

    def test_init_maze(self) -> None:
        maze = DepthFirstSearch.init_maze(10, 10)
        cell = Cell(value=15)
        maze[1][1].set_est(False)
        assert maze[0][0].value == cell.value

    def test_rand_cells(self) -> None:
        w_h = (10, 10)
        lst = DepthFirstSearch.add_cell_visited((0, 0))
        rand_cells = DepthFirstSearch.random_cells(lst, (0, 1), w_h)
        assert len(rand_cells) == 2

    def test_next_cell(self) -> None:
        coord = (5, 4)
        x, y = coord
        assert DepthFirstSearch.next_cell(x, y, "N") == (5, 3)

    def test_reverse_path(self) -> None:
        assert DepthFirstSearch.reverse_path("N") == "S"

    def test_last(self) -> None:
        lst = [(0, 0), (1, 1)]
        assert DepthFirstSearch.last(lst) == (1, 1)

    def test_BOS(self) -> None:
        path = [(0, 0), (0, 2), (1, 1)]
        assert len(DepthFirstSearch.random_cells(path, (0, 1), (10, 10))) == 0
