import numpy
from mazegen import Cell
from mazegen import Maze


def test_maze_setter_getter() -> None:
    maze = Maze(numpy.array([]))

    test = numpy.array(
        [
            [Cell(value=6), Cell(value=8), Cell(value=11)],
            [Cell(value=6), Cell(value=8), Cell(value=11)],
            [Cell(value=6), Cell(value=8), Cell(value=11)],
        ]
    )

    maze.set_maze(test)
    m = maze.get_maze()
    assert m is not None
    assert numpy.array_equal(m, test) is True


def test_maze_str() -> None:
    test = numpy.array(
        [
            [Cell(value=6), Cell(value=8), Cell(value=11)],
            [Cell(value=6), Cell(value=8), Cell(value=11)],
            [Cell(value=6), Cell(value=8), Cell(value=11)],
        ]
    )
    maze = Maze(test)

    assert maze.__str__() == "68B\n68B\n68B\n"
