from typing import Any
from numpy.typing import NDArray
from src.AMazeIng import AMazeIng
from src.parsing import Parsing
from mlx import Mlx
import time


class MazeMLX:
    """Render, animate, and interact with a maze using an MLX window."""

    def __init__(self, height: int, width: int) -> None:
        """Initialize the MLX renderer and create the window and image buffer.

        Args:
            height: Height of the rendering area in pixels.
            width: Width of the rendering area in pixels.
        """
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

    def close(self) -> None:
        """Destroy the image used by the renderer."""
        self.mlx.mlx_destroy_image(self.mlx_ptr, self.img_ptr)

    def close_loop(self, _: Any) -> None:
        """Stop the MLX event loop.

        Args:
            _: Unused callback argument.
        """
        self.mlx.mlx_loop_exit(self.mlx_ptr)

    def clear_image(self) -> None:
        """Clear the image buffer."""
        self.buf[:] = b"\x00" * len(self.buf)

    def redraw_image(self) -> None:
        """Redraw the window contents and display the control help text."""
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

    def put_pixel(
        self, x: int, y: int, color: list[Any] | None = None
    ) -> None:
        """Draw a single pixel into the image buffer.

        Args:
            x: Horizontal pixel position.
            y: Vertical pixel position.
            color: Optional RGBA color list. If omitted, the current renderer
                color is used.
        """
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return
        offset = y * self.size_line + x * (self.bpp // 8)

        if color:
            self.buf[offset + 0] = color[0]
            self.buf[offset + 1] = color[1]
            self.buf[offset + 2] = color[2]
            if self.bpp >= 32:
                self.buf[offset + 3] = color[3]
        else:
            self.buf[offset + 0] = self.color[0]
            self.buf[offset + 1] = self.color[1]
            self.buf[offset + 2] = self.color[2]
            if self.bpp >= 32:
                self.buf[offset + 3] = self.color[3]

    def put_line(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        color: list[Any] | None = None,
    ) -> None:
        """Draw a horizontal or vertical line.

        Args:
            start: Starting pixel coordinates.
            end: Ending pixel coordinates.
            color: Optional RGBA color list.
        """
        sx, sy = start
        ex, ey = end
        if sy == ey:
            for x in range(min(sx, ex), max(sx, ex) + 1):
                self.put_pixel(x, sy, color)
        if sx == ex:
            for y in range(min(sy, ey), max(sy, ey) + 1):
                self.put_pixel(sx, y, color)

    def put_block(
        self,
        ul: tuple[int, int],
        dr: tuple[int, int],
        color: list[Any] | None = None,
    ) -> None:
        """Draw a filled rectangular block.

        Args:
            ul: Upper-left corner coordinates.
            dr: Lower-right corner coordinates.
            color: Optional RGBA color list.
        """
        for y in range(min(ul[1], dr[1]), max(dr[1], ul[1])):
            self.put_line(
                (min(ul[0], dr[0]), y), (max(ul[0], dr[0]), y), color
            )

    @staticmethod
    def random_color_ft() -> Any:
        """Yield colors in a repeating sequence for the reserved pattern.

        Yields:
            RGBA color lists.
        """
        colors = [
            [0xFF, 0xBF, 0x00, 0xFF],  # blue
            [0x00, 0xFF, 0x40, 0xFF],  # green
            [0xFF, 0x00, 0xFF, 0xFF],  # pink
            [0x00, 0xFF, 0xFF, 0xFF],  # yellow
        ]
        while True:
            for color in colors:
                yield color

    @staticmethod
    def random_color() -> Any:
        """Yield colors in a repeating sequence for maze rendering.

        Yields:
            RGBA color lists.
        """
        colors = [
            [0xFF, 0x00, 0xFF, 0xFF],  # pink
            [0x00, 0xFF, 0xFF, 0xFF],  # yellow
            [0x00, 0xFF, 0x40, 0xFF],  # green
            [0xFF, 0xBF, 0x00, 0xFF],  # blue
            [0xFF, 0x00, 0x80, 0xFF],  # purple
            [0x00, 0x00, 0xFF, 0xFF],  # red
        ]
        while True:
            for color in colors:
                yield color

    def get_margin_line_len(self, maze: NDArray[Any]) -> tuple[int, int, int]:
        """Compute the cell size and margins for centering the maze.

        Args:
            maze: Maze grid to render.

        Returns:
            A tuple containing the cell side length, horizontal margin, and
            vertical margin.
        """
        rows = len(maze)
        cols = len(maze[0])

        line_len = min(self.width // cols, self.height // rows) - 1

        maze_width = cols * line_len
        maze_height = rows * line_len

        margin_x = ((self.width - maze_width) // 2) + 1
        margin_y = ((self.height - maze_height) // 2) + 1

        return (line_len, margin_x, margin_y)

    def update_maze(self, maze: NDArray[Any]) -> None:
        """Render the maze walls into the image buffer.

        Args:
            maze: Maze grid to render.
        """
        self.clear_image()

        line_len, margin_x, margin_y = self.get_margin_line_len(maze)
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
        """Animate the solution path inside the maze.

        Args:
            amazing: Maze container with generation and solving logic.

        Yields:
            Control after each path segment so the animation can be rendered
            progressively.
        """
        path = amazing.solve_path()
        print(path)
        actual = amazing.entry
        actual = (actual[0] - 1, actual[1] - 1)
        maze = amazing.maze.get_maze()
        if maze is None:
            return

        line_len, margin_x, margin_y = self.get_margin_line_len(maze)

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

    def put_start_end(self, amazing: AMazeIng) -> None:
        """Draw highlighted blocks for the maze entry and exit.

        Args:
            amazing: Maze container with current maze data.
        """
        entry = amazing.entry
        exit = amazing.exit
        maze = amazing.maze.get_maze()
        if maze is None:
            return

        line_len, margin_x, margin_y = self.get_margin_line_len(maze)

        ul = (
            (entry[0] - 1) * line_len + margin_x + 3,
            (entry[1] - 1) * line_len + 3 + margin_y,
        )
        dr = (
            (entry[0] - 1) * line_len + line_len + margin_x - 3,
            (entry[1] - 1) * line_len + line_len - 3 + margin_y,
        )
        self.put_block(ul, dr, [0xFF, 0xBF, 0x00, 0x9F])

        ul = (
            (exit[0] - 1) * line_len + margin_x + 3,
            (exit[1] - 1) * line_len + 3 + margin_y,
        )
        dr = (
            (exit[0] - 1) * line_len + line_len + margin_x - 3,
            (exit[1] - 1) * line_len + line_len - 3 + margin_y,
        )
        self.put_block(ul, dr, [0x00, 0xFF, 0x40, 0x9F])

    def draw_ft(
        self, maze: NDArray[Any], color: list[Any] | None = None
    ) -> None:
        """Draw filled cells corresponding to the reserved fully walled pattern.

        Args:
            maze: Maze grid to inspect.
            color: Optional RGBA color list.
        """
        line_len, margin_x, margin_y = self.get_margin_line_len(maze)

        for y in range(len(maze)):
            for x in range(len(maze[0])):
                if maze[y][x].value == 15:
                    x0 = x * line_len + margin_x
                    y0 = y * line_len + margin_y
                    x1 = x * line_len + line_len + margin_x
                    y1 = y * line_len + line_len + margin_y
                    self.put_block((x0, y0), (x1, y1), color)

    def draw_image(self, amazing: AMazeIng) -> None:
        maze = amazing.maze.get_maze()
        """Main rendering callback used by the MLX loop.

        Args:
            amazing: Maze container to render.
        """
        if self.render_maze(amazing):
            if self.print_path:
                if self.render_path():
                    color = next(self.color_gen_ft)
                    if maze is not None:
                        self.draw_ft(maze, color)
                    next(self.timer_gen)
            else:
                self.time_gen()
                if maze is not None:
                    self.update_maze(maze)
                    self.draw_ft(maze)
            self.put_start_end(amazing)
        self.redraw_image()

    def shift_color(self) -> None:
        """Reset the maze color generator."""
        self.color_gen = self.random_color()

    def shift_color_ft(self) -> None:
        """Reset the reserved-pattern color generator."""
        self.color_gen_ft = self.random_color_ft()

    def time_gen(self) -> None:
        """Reset the timing generator used for animation pacing."""
        self.timer_gen = self.time_generator()

    def restart_maze(self, amazing: AMazeIng) -> None:
        """Restart maze generation.

        Args:
            amazing: Maze container providing the generation generator.
        """
        self.generator = amazing.generate()

    def time_generator(self) -> Any:
        """Yield regularly with a fixed delay for animation timing.

        Yields:
            ``None`` at each step after sleeping.
        """
        yield
        while True:
            time.sleep(0.3)
            yield

    def restart_path(self, amazing: AMazeIng) -> None:
        """Restart solution path animation.

        Args:
            amazing: Maze container providing the solution path.
        """
        self.path_printer = self.put_path(amazing)

    def render_path(self) -> bool:
        """Advance the path animation by one step.

        Returns:
            ``True`` if the path animation is complete, otherwise ``False``.
        """
        try:
            next(self.path_printer)
            time.sleep(0.03)
            return False
        except StopIteration:
            pass
        return True

    def render_maze(self, amazing: AMazeIng) -> bool:
        """Advance maze generation by one step and redraw it.

        Args:
            amazing: Maze container being generated.

        Returns:
            ``True`` if maze generation is complete, otherwise ``False``.
        """
        try:
            maze = amazing.maze.get_maze()
            next(self.generator)
            if maze is not None:
                self.update_maze(maze)
            return False
        except StopIteration:
            pass
        return True

    def handle_key_press(self, keycode: int, amazing: AMazeIng) -> None:
        """Handle keyboard input for one keycode mapping.

        Args:
            keycode: Key code received from MLX.
            amazing: Maze container to update or render.
        """
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

    def handle_key_press_mteriier(
        self, keycode: int, amazing: AMazeIng
    ) -> None:
        """Handle keyboard input for an alternative keycode mapping.

        Args:
            keycode: Key code received from MLX.
            amazing: Maze container to update or render.
        """
        if keycode == 38:
            self.restart_maze(amazing)
            self.print_path = False
        if keycode == 233:
            self.restart_path(amazing)
            self.print_path = True if self.print_path is False else False
        if keycode == 34:
            self.print_path = False
            self.color = next(self.color_gen)
        if keycode == 39:
            self.close_loop(None)

    def start(self, amazing: AMazeIng) -> None:
        """Start the MLX rendering loop.

        Args:
            amazing: Maze container to generate, solve, and display.
        """
        self.restart_maze(amazing)
        self.shift_color()
        self.shift_color_ft()
        self.time_gen()
        self.mlx.mlx_loop_hook(self.mlx_ptr, self.draw_image, amazing)
        self.mlx.mlx_hook(self.win_ptr, 33, 0, self.close_loop, None)
        self.mlx.mlx_hook(
            self.win_ptr, 2, 1 << 0, self.handle_key_press, amazing
        )
        self.mlx.mlx_loop(self.mlx_ptr)


def main() -> None:
    """Run the maze application."""
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
