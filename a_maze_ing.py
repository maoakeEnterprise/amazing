import os
from src.amaz_lib import Maze
from src.amaz_lib import MazeGenerator
import src.amaz_lib as g


def main(maze_gen: MazeGenerator) -> None:
    # try:
    maze = Maze(maze=None)
    for alg in maze_gen.generator(5, 2):
        maze.set_maze(alg)
    os.system("clear")
    maze.ascii_print()


# except Exception as err:
# print(err)


if __name__ == "__main__":
    main(g.DepthFirstSearch((1, 1), (1, 1), False))
