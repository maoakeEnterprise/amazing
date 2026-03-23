from amaz_lib.MazeGenerator import DepthFirstSearch
from amaz_lib.Cell import Cell


class TestDepth:

    def test_init_maze(self) -> None:
        maze = DepthFirstSearch.init_maze(10, 10)
        cell = Cell(value=15)
        maze[1][1].set_est(False)
        assert maze[0][0].value == cell.value

    def test_rand_cells(self) -> None:
        maze = DepthFirstSearch.init_maze(10, 10)
        lst = DepthFirstSearch.add_cell_visited(maze[0][0])
        rand_cells = DepthFirstSearch.random_cells(lst, maze, 0, 1)
        assert len(rand_cells) == 2
