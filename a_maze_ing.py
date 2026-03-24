import os
from src.amaz_lib import Kruskal
from src.amaz_lib import DepthFirstSearch
from src.amaz_lib import Maze


def main() -> None:
    # try:
    maze = Maze(maze=None)
    gen = Kruskal().generator(10, 10)
    for alg in gen:
        maze.set_maze(alg)
        os.system("clear")
        maze.ascii_print()


def main2() -> None:
    maze = Maze(maze=None)
    gen = DepthFirstSearch.generator(50, 50)
    maze.set_maze(gen)
    os.system("clear")
    maze.ascii_print()


# except Exception as err:
# print(err)


if __name__ == "__main__":
    main2()
