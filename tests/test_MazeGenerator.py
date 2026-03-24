import numpy
from amaz_lib.MazeGenerator import DepthFirstSearch
from amaz_lib.MazeGenerator import Kruskal


class TestMazeGenerator:

    def test_kruskal_output_shape() -> None:
        generator = Kruskal().generator(10, 10)
        maze = numpy.array([])
        for output in generator:
            maze = output

        assert maze.shape == (10, 10)

    def test_generator(self) -> None:
        maze = numpy.array([])
        maze = DepthFirstSearch.generator(10, 10)
        assert maze.shape == (10, 10)
