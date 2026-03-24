import os
from numpy import ma
from src.amaz_lib import MazeGenerator, Kruskal, AStar
from src.amaz_lib import Maze


def main() -> None:
    # try:
    maze = Maze(maze=None)
    generator = Kruskal()
    for alg in generator.generator(20, 20):
        maze.set_maze(alg)
        os.system("clear")
        maze.ascii_print()
    solver = AStar((1, 1), (14, 18))
    print(solver.solve(maze))


# except Exception as err:
# print(err)


if __name__ == "__main__":
    main()
