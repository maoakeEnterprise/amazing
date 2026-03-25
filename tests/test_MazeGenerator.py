import numpy
from amaz_lib.MazeGenerator import DepthFirstSearch, MazeGenerator


class TestMazeGenerator:

    def test_generator(self) -> None:
        w_h = (10, 10)
        maze = numpy.array([])
        generator = DepthFirstSearch((1, 1), (2, 2), True).generator(*w_h)
        for output in generator:
            maze = output

        assert maze.shape == w_h

    def test_gen_broken(self) -> None:
        test = MazeGenerator.gen_broken_set(50, 50)
        assert len(test) > 0
