import os
from src.amaz_lib import Maze
from src.amaz_lib import MazeGenerator
import src.amaz_lib as g


def main(maze_gen: MazeGenerator) -> None:
    # try:
    maze = Maze(maze=None)
    gen = maze_gen.generator(100, 100)
    for alg in gen:
        maze.set_maze(alg)
        os.system("clear")
        maze.ascii_print()

# except Exception as err:
# print(err)


if __name__ == "__main__":
    main(g.DepthFirstSearch())
