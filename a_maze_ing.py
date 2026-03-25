import os
from src.amaz_lib import Maze
from src.amaz_lib import MazeGenerator
import src.amaz_lib as g


def main(maze_gen: MazeGenerator) -> None:
    # try:
    maze = Maze(maze=None)
    solver = g.DepthFirstSearchSolver((1, 1), (8, 5))
    for alg in maze_gen.generator(15, 15):
        maze.set_maze(alg)
        os.system("clear")
    maze.ascii_print()
    print(solver.solve(maze, 15, 15))
    # solver = AStar((1, 1), (14, 18))
    # print(solver.solve(maze))


# except Exception as err:
# print(err)


if __name__ == "__main__":
    main(g.DepthFirstSearch((1, 1), (8, 5)))
