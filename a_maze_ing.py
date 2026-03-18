from numpy import ma
from src.amaz_lib import kruskal
from src.amaz_lib import Maze


def main() -> None:
    try:
        maze = Maze(maze=None)
        for alg in kruskal(10, 10):
            maze.set_maze(alg)
        maze.export_maze("test.txt")
    except Exception as err:
        print(err)


if __name__ == "__main__":
    main()
