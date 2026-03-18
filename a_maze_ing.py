from src.amaz_lib import MazeGenerator
from src.amaz_lib import Maze


def main() -> None:
    try:
        maze = Maze(maze=None, start=(1, 1), end=(16, 15))
        for alg in MazeGenerator.Kruskal.kruskal(20, 20):
            maze.set_maze(alg)
        maze.export_maze("test.txt")
    except Exception as err:
        print(err)


if __name__ == "__main__":
    main()
