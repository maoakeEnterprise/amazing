from abc import ABC, abstractmethod
from typing import Generator, Any
from mazegen import Maze
import numpy as np
from numpy.typing import NDArray
from mazegen.Cell import Cell
import math
import random


class MazeGenerator(ABC):
    """Define the common interface and helpers for maze generators."""

    def __init__(
        self, start: tuple[int, int], end: tuple[int, int], perfect: bool
    ) -> None:
        """Initialize the maze generator.

        Args:
            start: Starting cell coordinates, using 1-based indexing.
            end: Ending cell coordinates, using 1-based indexing.
            perfect: Whether to generate a perfect maze with no loops.
        """
        self.start = (start[1] - 1, start[0] - 1)
        self.end = (end[1] - 1, end[0] - 1)
        self.perfect = perfect

    @abstractmethod
    def generator(
        self, height: int, width: int, seed: int | None = None
    ) -> Generator[NDArray[Any], None, NDArray[Any]]:
        """Generate a maze step by step.

        Args:
            height: Number of rows in the maze.
            width: Number of columns in the maze.
            seed: Optional random seed for reproducibility.

        Yields:
            Intermediate maze states during generation.

        Returns:
            The final generated maze.
        """
        ...

    @staticmethod
    def get_cell_ft(width: int, height: int) -> set[tuple[int, int]]:
        """Return the coordinates used to reserve the '42' pattern.

        Args:
            width: Number of columns in the maze.
            height: Number of rows in the maze.

        Returns:
            A set of cell coordinates belonging to the reserved pattern.
        """
        forty_two = set()
        y, x = (int(height / 2), int(width / 2))
        forty_two.add((y, x - 1))
        forty_two.add((y, x - 2))
        forty_two.add((y, x - 3))
        forty_two.add((y - 1, x - 3))
        forty_two.add((y - 2, x - 3))
        forty_two.add((y + 1, x - 1))
        forty_two.add((y + 2, x - 1))
        forty_two.add((y, x + 1))
        forty_two.add((y, x + 2))
        forty_two.add((y, x + 3))
        forty_two.add((y - 1, x + 3))
        forty_two.add((y - 2, x + 3))
        forty_two.add((y - 2, x + 2))
        forty_two.add((y - 2, x + 1))
        forty_two.add((y + 1, x + 1))
        forty_two.add((y + 2, x + 1))
        forty_two.add((y + 2, x + 2))
        forty_two.add((y + 2, x + 3))
        return forty_two

    @staticmethod
    def unperfect_maze(
        width: int,
        height: int,
        maze: NDArray[Any],
        forty_two: set[tuple[int, int]] | None,
        prob: float = 0.1,
    ) -> Generator[NDArray[Any], None, NDArray[Any]]:
        """Add extra openings to transform a perfect maze into an imperfect
        one.

        Random walls are removed while optionally preserving the reserved
            ``forty_two`` area.

        Args:
            width: Number of columns in the maze.
            height: Number of rows in the maze.
            maze: The maze to modify.
            forty_two: Optional set of reserved coordinates that must not be
                altered.
            prob: Probability of breaking an eligible wall.

        Yields:
            Intermediate maze states after each wall removal.

        Returns:
            The modified maze.
        """

        def enough_wall(cell: Cell) -> bool:
            nb_wall = 0
            if cell.get_est():
                nb_wall += 1
            if cell.get_north():
                nb_wall += 1
            if cell.get_west():
                nb_wall += 1
            if cell.get_south():
                nb_wall += 1
            if nb_wall == 3:
                return True
            return False

        directions = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "E": (1, 0)}

        reverse = {"N": "S", "S": "N", "W": "E", "E": "W"}
        min_break = 1
        while True:
            count = 0
            for y in range(height):
                for x in range(width):
                    if forty_two and (x, y) in forty_two:
                        continue
                    for direc, (dx, dy) in directions.items():
                        nx, ny = x + dx, y + dy
                        if forty_two and (
                            (y, x) in forty_two or (ny, nx) in forty_two
                        ):
                            continue
                        if not (0 <= nx < width and 0 < ny < height):
                            continue
                        if direc in ["S", "E"]:
                            continue
                        if not enough_wall(maze[y][x]):
                            continue
                        else:
                            count += 1
                            cell = maze[y][x]
                            cell_n = maze[ny][nx]
                            cell = DepthFirstSearch.broken_wall(cell, direc)
                            cell_n = DepthFirstSearch.broken_wall(
                                cell_n,
                                reverse[direc],
                            )
                            maze[y][x] = cell
                            maze[ny][nx] = cell_n
                        yield maze
            if count >= min_break:
                break
        return maze


class Kruskal(MazeGenerator):
    """Generate a maze using a Kruskal-based algorithm."""

    class KruskalSet:
        """Represent a connected component of maze cells."""

        def __init__(self, cells: list[int]) -> None:
            """Initialize a set of connected cells.

            Args:
                cells: List of cell indices belonging to the set.
            """
            self.cells: list[int] = cells

    class Sets:
        """Store all connected components used during generation."""

        def __init__(self, sets: list["Kruskal.KruskalSet"]) -> None:
            """Initialize the collection of connected components.

            Args:
                sets: List of disjoint cell sets.
            """
            self.sets = sets

    @staticmethod
    def walls_to_maze(
        walls: list[tuple[int, int]], height: int, width: int
    ) -> NDArray[Any]:
        """Convert a list of remaining walls into a maze grid.

        Args:
            walls: Collection of wall pairs between adjacent cells.
            height: Number of rows in the maze.
            width: Number of columns in the maze.

        Returns:
            A two-dimensional array of :class:`Cell` instances representing the
            maze.
        """

        maze: NDArray[Any] = np.array(
            [[Cell(value=0) for _ in range(width)] for _ in range(height)]
        )
        for wall in walls:
            x, y = wall
            match y - x:
                case 1:
                    maze[math.trunc((x / width))][x % width].set_est(True)
                    maze[math.trunc((y / width))][y % width].set_west(True)
                case width:
                    maze[math.trunc((x / width))][x % width].set_south(True)
                    maze[math.trunc((y / width))][y % width].set_north(True)
        for x in range(height):
            for y in range(width):
                if x == 0:
                    maze[x][y].set_north(True)
                if x == height - 1:
                    maze[x][y].set_south(True)
                if y == 0:
                    maze[x][y].set_west(True)
                if y == width - 1:
                    maze[x][y].set_est(True)
        return maze

    @staticmethod
    def is_in_same_set(sets: Sets, wall: tuple[int, int]) -> bool:
        """Check whether both cells connected by a wall are in the same set.

        Args:
            sets: Current collection of connected components.
            wall: Pair of adjacent cell indices.

        Returns:
            ``True`` if both cells belong to the same set, otherwise ``False``.
        """
        a, b = wall
        for set in sets.sets:
            if a in set.cells and b in set.cells:
                return True
            elif a in set.cells or b in set.cells:
                return False
        return False

    @staticmethod
    def merge_sets(sets: Sets, wall: tuple[int, int]) -> None:
        """Merge the two sets connected by the given wall.

        Args:
            sets: Current collection of connected components.
            wall: Pair of adjacent cell indices.

        Raises:
            Exception: If the two corresponding sets cannot be found.
        """
        a, b = wall
        base_set = None
        for i in range(len(sets.sets)):
            if base_set is None and (
                a in sets.sets[i].cells or b in sets.sets[i].cells
            ):
                base_set = sets.sets[i]
            elif base_set and (
                a in sets.sets[i].cells or b in sets.sets[i].cells
            ):
                base_set.cells += sets.sets[i].cells
                sets.sets.pop(i)
                return
        raise Exception("two sets not found")

    @staticmethod
    def touch_ft(
        width: int,
        wall: tuple[int, int],
        cells_ft: None | set[tuple[int, int]],
    ) -> bool:
        """Check whether a wall touches the reserved '42' pattern.

        Args:
            width: Number of columns in the maze.
            wall: Pair of adjacent cell indices.
            cells_ft: Reserved coordinates, or ``None``.

        Returns:
            ``True`` if either endpoint of the wall belongs to the reserved
            pattern, otherwise ``False``.
        """
        if cells_ft is None:
            return False
        s1 = (math.trunc(wall[0] / width), wall[0] % width)
        s2 = (math.trunc(wall[1] / width), wall[1] % width)
        return s1 in cells_ft or s2 in cells_ft

    def generator(
        self, height: int, width: int, seed: int | None = None
    ) -> Generator[NDArray[Any], None, NDArray[Any]]:
        """Generate a maze using a Kruskal-based approach.

        Args:
            height: Number of rows in the maze.
            width: Number of columns in the maze.
            seed: Optional random seed for reproducibility.

        Yields:
            Intermediate maze states during generation.

        Returns:
            The final generated maze.
        """
        cells_ft = None
        if height >= 7 and width >= 9:
            cells_ft = self.get_cell_ft(width, height)
        if cells_ft and (self.start in cells_ft or self.end in cells_ft):
            print(
                "Forty two will not be display. "
                "Entry or exit set in the ft logo"
            )
            cells_ft = None

        if seed is not None:
            np.random.seed(seed)
        sets = self.Sets([self.KruskalSet([i]) for i in range(height * width)])
        walls = []
        for h in range(height):
            for w in range(width - 1):
                walls += [(w + (width * h), w + (width * h) + 1)]
        for h in range(height - 1):
            for w in range(width):
                walls += [(w + (width * h), w + (width * (h + 1)))]
        np.random.shuffle(walls)

        yield self.walls_to_maze(walls, height, width)
        while (len(sets.sets) != 1 and cells_ft is None) or (
            len(sets.sets) != 19 and cells_ft is not None
        ):
            for wall in walls:
                if not self.is_in_same_set(sets, wall) and not self.touch_ft(
                    width, wall, cells_ft
                ):
                    self.merge_sets(sets, wall)
                    walls.remove(wall)
                    yield self.walls_to_maze(walls, height, width)
                if (len(sets.sets) == 1 and cells_ft is None) or (
                    len(sets.sets) == 19 and cells_ft is not None
                ):
                    break
        maze = self.walls_to_maze(walls, height, width)
        if self.perfect is False:
            gen = Kruskal.unperfect_maze(width, height, maze, cells_ft)
            for res in gen:
                maze = res
                yield maze
        return maze


class DepthFirstSearch(MazeGenerator):
    """Generate a maze using a depth-first search backtracking algorithm."""

    def __init__(
        self, start: tuple[int, int], end: tuple[int, int], perfect: bool
    ) -> None:
        """Initialize the depth-first search generator.

        Args:
            start: Starting cell coordinates, using 1-based indexing.
            end: Ending cell coordinates, using 1-based indexing.
            perfect: Whether to generate a perfect maze with no loops.
        """
        self.start = (start[1] - 1, start[0] - 1)
        self.end = (end[1] - 1, end[0] - 1)
        self.perfect = perfect
        self.forty_two: set[tuple[int, int]] | None = None

    def generator(
        self, height: int, width: int, seed: int | None = None
    ) -> Generator[NDArray[Any], None, NDArray[Any]]:
        """Generate a maze using depth-first search.

        Args:
            height: Number of rows in the maze.
            width: Number of columns in the maze.
            seed: Optional random seed for reproducibility.

        Yields:
            Intermediate maze states during generation.

        Returns:
            The final generated maze.
        """
        if seed is not None:
            random.seed(seed)
        maze = self.init_maze(width, height)
        if width >= 9 and height >= 7:
            self.forty_two = self.get_cell_ft(width, height)
        visited: NDArray[np.object_] = np.zeros((height, width), dtype=bool)
        if (
            self.forty_two
            and self.start not in self.forty_two
            and self.end not in self.forty_two
        ):
            visited = self.lock_cell_ft(visited, self.forty_two)
        else:
            print(
                "Forty two will not be display. "
                "Entry or exit set in the ft logo"
            )
        path: list[tuple[int, int]] = list()
        w_h = (width, height)
        coord = (0, 0)
        x, y = coord
        first_iteration = True

        while path or first_iteration:
            first_iteration = False

            visited[y, x] = True
            path = self.add_cell_visited(coord, path)

            random_c = self.random_cells(visited, coord, w_h)

            if not random_c:
                path = self.back_on_step(path, w_h, visited)
                if not path:
                    break
                coord = path[-1]
                random_c = self.random_cells(visited, coord, w_h)
                x, y = coord

            wall = self.next_step(random_c)
            maze[y][x] = self.broken_wall(maze[y][x], wall)

            coord = self.next_cell(x, y, wall)
            wall_r = self.reverse_path(wall)
            x, y = coord
            maze[y][x] = self.broken_wall(maze[y][x], wall_r)
            yield maze
        if self.perfect is False:
            gen = DepthFirstSearch.unperfect_maze(
                width,
                height,
                maze,
                self.forty_two,
            )
            for res in gen:
                maze = res
                yield maze
        return maze

    @staticmethod
    def init_maze(width: int, height: int) -> NDArray[Any]:
        """Create a fully walled maze grid.

        Args:
            width: Number of columns in the maze.
            height: Number of rows in the maze.

        Returns:
            A two-dimensional array of cells initialized with all
            walls present.
        """
        maze = np.array(
            [[Cell(value=15) for _ in range(width)] for _ in range(height)]
        )
        return maze

    @staticmethod
    def add_cell_visited(
        coord: tuple[int, int], path: list[tuple[int, int]]
    ) -> list[tuple[int, int]]:
        """Append a visited coordinate to the current traversal path.

        Args:
            coord: Coordinate of the visited cell.
            path: Current traversal path.

        Returns:
            The updated path.
        """
        path.append(coord)
        return path

    @staticmethod
    def random_cells(
        visited: NDArray[Any], coord: tuple[int, int], w_h: tuple[int, int]
    ) -> list[str]:
        """Return the list of unvisited neighboring directions.

        Args:
            visited: Boolean array marking visited cells.
            coord: Current cell coordinate.
            w_h: Tuple containing maze width and height.

        Returns:
            A list of direction strings among ``"N"``, ``"S"``, ``"W"``, and
            ``"E"``.
        """
        rand_cell: list[str] = []
        x, y = coord
        width, height = w_h

        if y - 1 >= 0 and not visited[y - 1][x]:
            rand_cell.append("N")

        if y + 1 < height and not visited[y + 1][x]:
            rand_cell.append("S")

        if x - 1 >= 0 and not visited[y][x - 1]:
            rand_cell.append("W")

        if x + 1 < width and not visited[y][x + 1]:
            rand_cell.append("E")
        return rand_cell

    @staticmethod
    def next_step(rand_cell: list[str]) -> str:
        """Select the next direction at random.

        Args:
            rand_cell: List of candidate directions.

        Returns:
            A randomly selected direction.
        """
        return random.choice(rand_cell)

    @staticmethod
    def broken_wall(cell: Cell, wall: str) -> Cell:
        """Remove the specified wall from a cell.

        Args:
            cell: The cell to modify.
            wall: Direction of the wall to remove.

        Returns:
            The modified cell.
        """
        if wall == "N":
            cell.set_north(False)
        elif wall == "S":
            cell.set_south(False)
        elif wall == "W":
            cell.set_west(False)
        elif wall == "E":
            cell.set_est(False)
        return cell

    @staticmethod
    def next_cell(x: int, y: int, next: str) -> tuple[int, int]:
        """Return the coordinates of the adjacent cell in the given direction.

        Args:
            x: Current column index.
            y: Current row index.
            next: Direction to move.

        Returns:
            The coordinates of the next cell.
        """
        next_step = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "E": (1, 0)}
        add_x, add_y = next_step[next]
        return (x + add_x, y + add_y)

    @staticmethod
    def reverse_path(direction: str) -> str:
        """Return the opposite cardinal direction.

        Args:
            direction: Input direction.

        Returns:
            The opposite direction.
        """
        return {"N": "S", "S": "N", "W": "E", "E": "W"}[direction]

    @staticmethod
    def back_on_step(
        path: list[tuple[int, int]],
        w_h: tuple[int, int],
        visited: NDArray[Any],
    ) -> list[tuple[int, int]]:
        """Backtrack through the path until a cell with unvisited neighbors
        is found.

        Args:
            path: Current traversal path.
            w_h: Tuple containing maze width and height.
            visited: Boolean array marking visited cells.

        Returns:
            The truncated path after backtracking.
        """
        while path:
            last = path[-1]
            if DepthFirstSearch.random_cells(visited, last, w_h):
                break
            path.pop()
        return path

    @staticmethod
    def lock_cell_ft(
        visited: NDArray[Any], forty_two: set[tuple[int, int]]
    ) -> NDArray[Any]:
        """Mark the reserved '42' pattern cells as already visited.

        Args:
            visited: Boolean array marking visited cells.
            forty_two: Set of reserved cell coordinates.

        Returns:
            The updated visited array.
        """
        tab = [cell for cell in forty_two]
        for cell in tab:
            visited[cell] = True
        return visited
