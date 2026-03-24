import numpy
from amaz_lib.MazeGenerator import DepthFirstSearch


class TestMazeGenerator:

    # def test_kruskal_output_shape() -> None:
    #     generator = Kruskal()
    #     maze = numpy.array([])
    #     for output in generator.generator(10, 10):
    #         maze = output

    #     assert maze.shape == (10, 10)

    def test_generator(self):
        maze = numpy.array([])
        maze = DepthFirstSearch.generator(10, 10)
        assert maze.shape == (10, 10)
