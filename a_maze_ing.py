from typing import Any
from src.AMazeIng import AMazeIng
from src.parsing import Parsing
from mlx import Mlx
import numpy as np
import math
import time


class MazeMLX:
    def __init__(self, height: int, width: int) -> None:
        self.mlx = Mlx()
        self.height = height
        self.width = width
        self.print_path = False
        self.color = [0x00, 0x00, 0xFF, 0xFF]
        self.mlx_ptr = self.mlx.mlx_init()
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr, width, height + 200, "A-Maze-Ing"
        )
        self.img_ptr = self.mlx.mlx_new_image(self.mlx_ptr, width, height)
        self.buf, self.bpp, self.size_line, self.format = (
            self.mlx.mlx_get_data_addr(self.img_ptr)
        )
        self.path_printer = None
        self.generator = None

    def close(self) -> None:
        self.mlx.mlx_destroy_image(self.mlx_ptr, self.img_ptr)

    def clear_image(self) -> None:
        self.buf[:] = b"\x00" * len(self.buf)

    def redraw_image(self) -> None:
        self.mlx.mlx_clear_window(self.mlx_ptr, self.win_ptr)
        self.mlx.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr, self.img_ptr, 0, 0
        )
        self.mlx.mlx_string_put(
            self.mlx_ptr,
            self.win_ptr,
            self.width // 3,
            self.height + 100,
            0xFFFFFF,
            "1: regen; 2: path; 3: color; 4: quit;",
        )

    def put_pixel(self, x, y) -> None:
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return
        offset = y * self.size_line + x * (self.bpp // 8)

        self.buf[offset + 0] = self.color[0]
        self.buf[offset + 1] = self.color[1]
        self.buf[offset + 2] = self.color[2]
        if self.bpp >= 32:
            self.buf[offset + 3] = self.color[3]

    def put_line(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        sx, sy = start
        ex, ey = end
        if sy == ey:
            for x in range(min(sx, ex), max(sx, ex) + 1):
                self.put_pixel(x, sy)
        if sx == ex:
            for y in range(min(sy, ey), max(sy, ey) + 1):
                self.put_pixel(sx, y)

    def put_block(self, ul: tuple[int, int], dr: tuple[int, int]) -> None:
        for y in range(min(ul[1], dr[1]), max(dr[1], ul[1])):
            self.put_line((min(ul[0], dr[0]), y), (max(ul[0], dr[0]), y))

    @staticmethod
    def random_color() -> Any:
        colors = [
            [0x00, 0x00, 0xFF, 0xFF],  # red
            [0x00, 0xFF, 0xFF, 0xFF],  # yellow
            [0x00, 0xFF, 0x40, 0xFF],  # green
            [0xFF, 0xBF, 0x00, 0xFF],  # blue
            [0xFF, 0x00, 0x80, 0xFF],  # purple
            [0xFF, 0x00, 0xFF, 0xFF],  # pink
        ]
        while True:
            for color in colors:
                yield color

    def update_maze(self, maze: np.ndarray) -> None:
        self.clear_image()

        rows = len(maze)
        cols = len(maze[0])

        line_len = min(self.width // cols, self.height // rows)

        maze_width = cols * line_len
        maze_height = rows * line_len

        margin_x = (self.width - maze_width) // 2
        margin_y = (self.height - maze_height) // 2
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                x0 = x * line_len + margin_x
                y0 = y * line_len + margin_y
                x1 = x * line_len + line_len + margin_x
                y1 = y * line_len + line_len + margin_y

                if maze[y][x].get_north():
                    self.put_line((x0, y0), (x1, y0))
                if maze[y][x].get_est():
                    self.put_line((x1, y0), (x1, y1))
                if maze[y][x].get_south():
                    self.put_line((x0, y1), (x1, y1))
                if maze[y][x].get_west():
                    self.put_line((x0, y0), (x0, y1))

    def put_path(self, amazing: AMazeIng) -> Any:
        path = amazing.solve_path()
        print(path)
        actual = amazing.entry
        actual = (actual[0] - 1, actual[1] - 1)
        maze = amazing.maze.get_maze()
        if maze is None:
            return

        rows = len(maze)
        cols = len(maze[0])

        line_len = min(self.width // cols, self.height // rows)

        maze_width = cols * line_len
        maze_height = rows * line_len

        margin_x = (self.width - maze_width) // 2
        margin_y = (self.height - maze_height) // 2

        for i in range(len(path)):
            ul = (
                (actual[0]) * line_len + margin_x + 12,
                (actual[1]) * line_len + 12 + margin_y,
            )
            dr = (
                (actual[0]) * line_len + line_len + margin_x - 12,
                (actual[1]) * line_len + line_len - 12 + margin_y,
            )
            self.put_block(ul, dr)
            x0 = actual[0] * line_len + margin_x + 12
            y0 = actual[1] * line_len + margin_y + 12
            x1 = actual[0] * line_len + line_len + margin_x - 12
            y1 = actual[1] * line_len + line_len + margin_y - 12
            yield
            match path[i]:
                case "N":
                    self.put_block((x0, y0), (x1, y0 - 24))
                    actual = (actual[0], actual[1] - 1)
                case "E":
                    self.put_block((x1, y0), (x1 + 24, y1))
                    actual = (actual[0] + 1, actual[1])
                case "S":
                    self.put_block((x0, y1), (x1, y1 + 24))
                    actual = (actual[0], actual[1] + 1)
                case "W":
                    self.put_block((x0, y0), (x0 - 24, y1))
                    actual = (actual[0] - 1, actual[1])
        ul = (
            (actual[0]) * line_len + margin_x + 12,
            (actual[1]) * line_len + 12 + margin_y,
        )
        dr = (
            (actual[0]) * line_len + line_len + margin_x - 12,
            (actual[1]) * line_len + line_len - 12 + margin_y,
        )
        self.put_block(ul, dr)
        return

    def put_start_end(self, amazing: AMazeIng):
        entry = amazing.entry
        exit = amazing.exit
        maze = amazing.maze.get_maze()
        if maze is None:
            return

        rows = len(maze)
        cols = len(maze[0])

        line_len = min(self.width // cols, self.height // rows)

        maze_width = cols * line_len
        maze_height = rows * line_len

        margin_x = (self.width - maze_width) // 2
        margin_y = (self.height - maze_height) // 2

        ul = (
            (entry[0]) * line_len + margin_x + 3,
            (entry[1]) * line_len + 3 + margin_y,
        )
        dr = (
            (entry[0]) * line_len + line_len + margin_x - 3,
            (entry[1]) * line_len + line_len - 3 + margin_y,
        )
        print(f"ul: {ul}; dr: {dr}")
        self.put_block(ul, dr)
        self.redraw_image()

    def draw_ft(self, maze: np.ndarray):
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
                if maze[y][x].value == 15:
                    self.put_block((x0, y0), (x1, y1))

    def close_loop(self, _: Any):
        self.mlx.mlx_loop_exit(self.mlx_ptr)

    def handle_key_press(self, keycode: int, amazing: AMazeIng) -> None:
        if keycode == 49:
            self.restart_maze(amazing)
            self.print_path = False
        if keycode == 50:
            self.restart_path(amazing)
            self.print_path = True if self.print_path is False else False
        if keycode == 51:
            self.print_path = False
            self.color = next(self.color_gen)
        if keycode == 52:
            self.close_loop(None)

    def draw_image(self, amazing: AMazeIng) -> None:
        if self.render_maze(amazing):
            if self.path_printer and self.print_path:
                self.render_path()
            else:
                self.draw_ft(amazing.maze.get_maze())
        self.redraw_image()

    def start(self, amazing: AMazeIng) -> None:
        self.restart_maze(amazing)
        self.shift_color()
        self.mlx.mlx_loop_hook(self.mlx_ptr, self.draw_image, amazing)
        self.mlx.mlx_hook(self.win_ptr, 33, 0, self.close_loop, None)
        self.mlx.mlx_hook(
            self.win_ptr, 2, 1 << 0, self.handle_key_press, amazing
        )
        self.mlx.mlx_loop(self.mlx_ptr)

    def restart_maze(self, amazing: AMazeIng) -> None:
        self.generator = amazing.generate()

    def restart_path(self, amazing: AMazeIng) -> None:
        self.path_printer = self.put_path(amazing)

    def shift_color(self):
        self.color_gen = self.random_color()

    def render_path(self):
        try:
            next(self.path_printer)
            time.sleep(0.03)
        except StopIteration:
            pass

    def render_maze(self, amazing: AMazeIng) -> bool:
        try:
            next(self.generator)
            self.update_maze(amazing.maze.get_maze())
            return False
        except StopIteration:
            self.put_start_end(amazing)
            pass
        return True


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
