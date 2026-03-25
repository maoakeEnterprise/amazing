import os
from src.AMazeIng import AMazeIng
from src.parsing import Parsing


def main() -> None:
    try:
        config = Parsing.DataMaze.get_data_maze("config.txt")
        print(config)
        amazing = AMazeIng(**config)
        for gen in amazing.generate():
            os.system("clear")
            amazing.maze.ascii_print()
    except Exception as err:
        print(err)


if __name__ == "__main__":
    main()
