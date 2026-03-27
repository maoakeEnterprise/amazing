import os
from typing import Any, Callable, Generator
from src.AMazeIng import AMazeIng
from src.parsing import Parsing
from mlx.mlx import Mlx
import numpy as np
import math
from src.amaz_lib import Maze
import time


class MazeMLX:
    def __init__(self, height: int, width: int) -> None:
        self.mlx = Mlx()
        self.height = height
        self.width = width
        self.mlx_ptr = self.mlx.mlx_init()
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr, width, height, "amazing"
        )
        self.img_ptr = self.mlx.mlx_new_image(self.mlx_ptr, width, height)
        self.buf, self.bpp, self.size_line, self.format = (
            self.mlx.mlx_get_data_addr(self.img_ptr)
        )

    def close(self) -> None:
        self.mlx.mlx_destroy_image(self.mlx_ptr, self.img_ptr)

    def put_pixel(self, x, y) -> None:
        offset = y * self.size_line + x * (self.bpp // 8)

        self.buf[offset + 0] = 0xFF
        self.buf[offset + 1] = 0xFF
        self.buf[offset + 2] = 0xFF
        if self.bpp >= 32:
            self.buf[offset + 3] = 0xFF

    def clear_image(self) -> None:
        self.buf[:] = b"\x00" * len(self.buf)

    def put_line(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        sx, sy = start
        ex, ey = end
        if sy == ey:
            for x in range(min(sx, ex), max(sx, ex) + 1):
                self.put_pixel(x, sy)
        if sx == ex:
            for y in range(min(sy, ey), max(sy, ey) + 1):
                self.put_pixel(sx, y)

    def update_maze(self, maze: np.ndarray) -> None:
        self.clear_image()
        margin = math.trunc(
            math.sqrt(self.width if self.width > self.height else self.height)
            // 2
        )
        line_len = math.trunc(
            (
                (self.height - margin) // len(maze)
                if self.height > self.width
                else (self.width - margin) // len(maze[0])
            )
        )
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                x0 = x * line_len + margin
                y0 = y * line_len + margin
                x1 = x * line_len + line_len + margin
                y1 = y * line_len + line_len + margin

                if maze[y][x].get_north():
                    self.put_line((x0, y0), (x1, y0))
                if maze[y][x].get_est():
                    self.put_line((x1, y0), (x1, y1))
                if maze[y][x].get_south():
                    self.put_line((x0, y1), (x1, y1))
                if maze[y][x].get_west():
                    self.put_line((x0, y0), (x0, y1))
        self.mlx.mlx_put_image_to_window(
                        self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0)

    def close_loop(self, _: Any):
        self.mlx.mlx_loop_exit(self.mlx_ptr)

    def gen_maze(self, amazing: AMazeIng) -> None:
        for output in amazing.generate():
            maze = output
            maze.ascii_print()
            self.clear_image()
            self.update_maze(amazing.maze.get_maze())

    def start(self, amazing: AMazeIng) -> None:
        test = self.gen_maze(amazing)
        # self.mlx.mlx_loop_hook(self.mlx_ptr, test, amazing)
        self.mlx.mlx_hook(self.win_ptr, 33, 0, self.close_loop, None)
        self.mlx.mlx_loop(self.mlx_ptr)


def main() -> None:
    mlx = None
    try:
        mlx = MazeMLX(1000, 1000)
        config = Parsing.DataMaze.get_data_maze("config.txt")
        amazing = AMazeIng(**config)
        mlx.start(amazing)
        with open("test.txt", "w") as output:
            output.write(amazing.__str__())
    except Exception as err:
        print(err)
    finally:
        if mlx is not None:
            mlx.close()


if __name__ == "__main__":
    main()
