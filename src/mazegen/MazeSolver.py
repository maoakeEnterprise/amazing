from abc import ABC, abstractmethod
from .Maze import Maze
from typing import Any
import numpy as np
from numpy.typing import NDArray
import random


class MazeSolver(ABC):
    """Define the common interface for maze-solving algorithms."""

    def __init__(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        """Initialize the maze solver.

        Args:
            start: Start coordinates using 1-based indexing.
            end: End coordinates using 1-based indexing.
        """
        self.start = (start[1] - 1, start[0] - 1)
        self.end = (end[1] - 1, end[0] - 1)

    @abstractmethod
    def solve(
        self, maze: Maze, height: int | None = None, width: int | None = None
    ) -> str:
        """Solve the maze and return the path as direction letters.

        Args:
            maze: The maze to solve.
            height: Optional maze height.
            width: Optional maze width.

        Returns:
            A string representing the path using cardinal directions.
        """
        ...


class AStar(MazeSolver):
    """Solve a maze using the A* pathfinding algorithm."""

    class Node:
        """Represent a node used during A* exploration."""

        def __init__(
            self,
            coordinate: tuple[int, int],
            g: int,
            h: int,
            f: int,
            parent: Any,
        ) -> None:
            """Initialize a search node.

            Args:
                coordinate: Coordinates of the node.
                g: Cost from the start node.
                h: Heuristic cost to the goal.
                f: Total estimated cost.
                parent: Parent node in the reconstructed path.
            """
            self.coordinate = coordinate
            self.g = g
            self.h = h
            self.f = f
            self.parent = parent

        def __eq__(self, value: object, /) -> bool:
            """Compare a node to a coordinate.

            Args:
                value: Object to compare with.

            Returns:
                ``True`` if the value equals the node coordinate, otherwise
                ``False``.
            """
            return value == self.coordinate

    def __init__(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        """Initialize the A* solver.

        Args:
            start: Start coordinates using 1-based indexing.
            end: End coordinates using 1-based indexing.
        """
        self.start = (start[0] - 1, start[1] - 1)
        self.end = (end[0] - 1, end[1] - 1)

    def h(self, n: tuple[int, int]) -> int:
        """Compute the Manhattan distance heuristic to the goal.

        Args:
            n: Coordinates of the current node.

        Returns:
            The heuristic distance to the end coordinate.
        """
        return (
            max(n[0], self.end[0])
            - min(n[0], self.end[0])
            + max(n[1], self.end[1])
            - min(n[1], self.end[1])
        )

    def get_paths(
        self,
        maze: NDArray[Any],
        actual: tuple[int, int],
        close: list["Node"],
    ) -> list[tuple[int, int]]:
        """Return all reachable neighboring coordinates.

        Args:
            maze: Maze grid to inspect.
            actual: Current coordinate.
            close: List of already explored nodes.

        Returns:
            A list of reachable adjacent coordinates not yet closed.
        """
        path = [
            (
                (actual[0], actual[1] - 1)
                if not maze[actual[1]][actual[0]].get_north()
                and actual[1] > 0
                and (actual[0], actual[1] - 1)
                not in [n.coordinate for n in close]
                else None
            ),
            (
                (actual[0] + 1, actual[1])
                if not maze[actual[1]][actual[0]].get_est()
                and actual[0] < len(maze[0]) - 1
                and (actual[0] + 1, actual[1])
                not in [n.coordinate for n in close]
                else None
            ),
            (
                (actual[0], actual[1] + 1)
                if not maze[actual[1]][actual[0]].get_south()
                and actual[1] < len(maze) - 1
                and (actual[0], actual[1] + 1)
                not in [n.coordinate for n in close]
                else None
            ),
            (
                (actual[0] - 1, actual[1])
                if not maze[actual[1]][actual[0]].get_west()
                and actual[0] > 0
                and (actual[0] - 1, actual[1])
                not in [n.coordinate for n in close]
                else None
            ),
        ]
        return [p for p in path if p is not None]

    def get_path(self, maze: NDArray[Any]) -> list["Node"]:
        """Perform A* exploration until the destination is reached.

        Args:
            maze: Maze grid to solve.

        Returns:
            The closed list ending with the goal node.

        Raises:
            Exception: If no path can be found.
        """
        open: list[AStar.Node] = []
        close: list[AStar.Node] = []

        open.append(
            AStar.Node(
                self.start,
                0,
                self.h(self.start),
                self.h(self.start),
                None,
            )
        )

        while len(open) > 0:
            to_check = sorted(open, key=lambda x: x.f)[0]
            open.remove(to_check)
            close.append(to_check)
            if to_check.coordinate == self.end:
                return close
            paths = self.get_paths(maze, to_check.coordinate, close)
            for path in paths:
                open.append(
                    self.Node(
                        path,
                        to_check.g + 1,
                        self.h(path),
                        self.h(path) + to_check.g + 1,
                        to_check,
                    )
                )
                if path == self.end:
                    break
        raise Exception("Path not found")

    def get_rev_dir(self, current: Node) -> str:
        """Determine the direction taken from the parent to the current node.

        Args:
            current: Current node in the reconstructed path.

        Returns:
            A cardinal direction letter.

        Raises:
            Exception: If the parent-child relationship cannot be translated.
        """
        if current.parent.coordinate == (
            current.coordinate[0],
            current.coordinate[1] - 1,
        ):
            return "S"
        elif current.parent.coordinate == (
            current.coordinate[0] + 1,
            current.coordinate[1],
        ):
            return "W"
        elif current.parent.coordinate == (
            current.coordinate[0],
            current.coordinate[1] + 1,
        ):
            return "N"
        elif current.parent.coordinate == (
            current.coordinate[0] - 1,
            current.coordinate[1],
        ):
            return "E"
        else:
            raise Exception("Translate error: AStar path not found")

    def translate(self, close: list["Node"]) -> str:
        """Translate a node chain into a path string.

        Args:
            close: Closed list ending with the goal node.

        Returns:
            A string of direction letters from start to end.
        """
        current = close[-1]
        res = ""
        while True:
            res = self.get_rev_dir(current) + res
            current = current.parent
            if current.coordinate == self.start:
                break
        return res

    def solve(
        self, maze: Maze, height: int | None = None, width: int | None = None
    ) -> str:
        """Solve the maze using A*.

        Args:
            maze: The maze to solve.
            height: Unused optional maze height.
            width: Unused optional maze width.

        Returns:
            A string representing the path using cardinal directions.
        """

        maze_arr = maze.get_maze()
        if maze_arr is None:
            raise Exception("Maze is not initialized")
        path: list[AStar.Node] = self.get_path(maze_arr)
        return self.translate(path)


class DepthFirstSearchSolver(MazeSolver):
    """Solve a maze using depth-first search with backtracking."""

    def __init__(self, start: tuple[int, int], end: tuple[int, int]):
        """Initialize the depth-first search solver.

        Args:
            start: Start coordinates using 1-based indexing.
            end: End coordinates using 1-based indexing.
        """
        super().__init__(start, end)

    def solve(
        self, maze: Maze, height: int | None = None, width: int | None = None
    ) -> str:
        """Solve the maze using depth-first search.

        Args:
            maze: The maze to solve.
            height: Maze height.
            width: Maze width.

        Returns:
            A string representing the path using cardinal directions.

        Raises:
            Exception: If no path can be found.
        """
        path_str = ""
        if height is None or width is None:
            raise Exception("We need Height and Width in the arg")
        visited: NDArray[Any] = np.zeros((height, width), dtype=bool)
        path: list[tuple[int, int]] = list()
        move: list[str] = list()
        maze_s = maze.get_maze()
        if maze_s is None:
            raise Exception("Maze is not initializef")
        coord = self.start
        h_w: tuple[int, int] = (height, width)
        while coord != self.end:
            visited[coord] = True
            path.append(coord)
            rand_p: list[str] = self.random_path(visited, coord, maze_s, h_w)

            if not rand_p:
                path, move = self.back_on_step(
                    path, visited, maze_s, h_w, move
                )
                if not path:
                    break
                coord = path[-1]
                rand_p = self.random_path(visited, coord, maze_s, h_w)
            next = self.next_path(rand_p)
            move.append(next)
            coord = self.next_cell(coord, next)
        for m in move:
            path_str += m
        if not path:
            raise Exception("Path not found")
        return path_str

    @staticmethod
    def random_path(
        visited: NDArray[Any],
        coord: tuple[int, int],
        maze: NDArray[Any],
        h_w: tuple[int, int],
    ) -> list[str]:
        """Return all valid unvisited directions from the current cell.

        Args:
            visited: Boolean array marking visited cells.
            coord: Current coordinate.
            maze: Maze grid to inspect.
            h_w: Tuple containing maze height and width.

        Returns:
            A list of valid direction letters.
        """
        random_p = []
        h, w = h_w
        y, x = coord

        if y - 1 >= 0 and not maze[y][x].get_north() and not visited[y - 1][x]:
            random_p.append("N")

        if y + 1 < h and not maze[y][x].get_south() and not visited[y + 1][x]:
            random_p.append("S")

        if x - 1 >= 0 and not maze[y][x].get_west() and not visited[y][x - 1]:
            random_p.append("W")

        if x + 1 < w and not maze[y][x].get_est() and not visited[y][x + 1]:
            random_p.append("E")
        return random_p

    @staticmethod
    def next_path(rand_path: list[str]) -> str:
        """Select the next move at random.

        Args:
            rand_path: List of available directions.

        Returns:
            A randomly selected direction.
        """

        return random.choice(rand_path)

    @staticmethod
    def back_on_step(
        path: list[tuple[int, int]],
        visited: NDArray[Any],
        maze: NDArray[Any],
        h_w: tuple[int, int],
        move: list[str],
    ) -> tuple[list[Any], list[Any]]:
        """Backtrack until a cell with an unexplored path is found.

        Args:
            path: Current path of visited coordinates.
            visited: Boolean array marking visited cells.
            maze: Maze grid to inspect.
            h_w: Tuple containing maze height and width.
            move: List of moves made so far.

        Returns:
            A tuple containing the updated path and move list.
        """

        while path:
            last = path[-1]
            if DepthFirstSearchSolver.random_path(visited, last, maze, h_w):
                break
            path.pop()
            move.pop()
        return path, move

    @staticmethod
    def next_cell(coord: tuple[int, int], next: str) -> tuple[int, int]:
        """Return the coordinates of the next cell in the given direction.

        Args:
            coord: Current coordinate.
            next: Direction to move.

        Returns:
            The coordinates of the next cell.
        """
        y, x = coord
        next_step = {"N": (-1, 0), "S": (1, 0), "W": (0, -1), "E": (0, 1)}
        add_y, add_x = next_step[next]
        return (y + add_y, x + add_x)
