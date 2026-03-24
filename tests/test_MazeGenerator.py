import numpy
from amaz_lib.MazeGenerator import DepthFirstSearch


class TestMazeGenerator:

    def test_generator(self) -> None:
        w_h = (300, 300)
        maze = numpy.array([])
        generator = DepthFirstSearch().generator(*w_h)
        for output in generator:
            maze = output

        assert maze.shape == w_h
