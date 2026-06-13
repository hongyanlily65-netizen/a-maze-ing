"""Maze object and wall operations."""

import random
from enum import IntEnum

from .pattern42 import add_42_pattern
from .prim import generate_prim


class Wall(IntEnum):
    """Bit values used to store the four walls of a cell."""

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


class MazeGenerator:
    """Generate and manipulate a maze using randomized Prim's algorithm.

    Attributes:
        width: Number of maze columns.
        height: Number of maze rows.
        entry: Entry coordinate.
        exit: Exit coordinate.
        perfect: Whether generation should avoid loops.
        seed: Random seed, where ``"0"`` requests a non-deterministic seed.
        grid: Generated grid of wall bitmasks.
        pattern42: Coordinates reserved for the closed-cell 42 pattern.
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_pos: tuple[int, int],
        perfect: bool = True,
        seed: str = "0",
    ) -> None:
        """Initialize a maze generator.

        Args:
            width: Number of maze columns.
            height: Number of maze rows.
            entry: Entry coordinate as an ``(x, y)`` pair.
            exit_pos: Exit coordinate as an ``(x, y)`` pair.
            perfect: Whether generation should avoid creating loops.
            seed: Random seed, where ``"0"`` requests a non-deterministic seed.
        """
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit_pos
        self.perfect = perfect
        self.seed = seed
        self.grid: list[list[int]] = []
        self.pattern42: set[tuple[int, int]] = set()

    def generate(self) -> list[list[int]]:
        """Create a new maze grid.

        Returns:
            The generated grid, whose cells contain wall bitmasks.

        Raises:
            ValueError: If the 42 pattern prevents connected generation.
        """
        random.seed(None if self.seed == "0" else self.seed)
        self.grid = [
            [15 for _ in range(self.width)] for _ in range(self.height)
        ]
        self.pattern42 = add_42_pattern(self)
        generate_prim(self)
        return self.grid

    def neighbor(
        self, cell: tuple[int, int], wall: Wall
    ) -> tuple[int, int]:
        """Return the coordinate adjacent to a cell in one direction.

        Args:
            cell: Source coordinate.
            wall: Direction from the source cell.

        Returns:
            The neighboring coordinate, which may be outside the maze.
        """
        x, y = cell
        moves = {
            Wall.NORTH: (x, y - 1),
            Wall.EAST: (x + 1, y),
            Wall.SOUTH: (x, y + 1),
            Wall.WEST: (x - 1, y),
        }
        return moves[wall]

    def inside(self, cell: tuple[int, int]) -> bool:
        """Check whether a coordinate is inside the maze.

        Args:
            cell: Coordinate to check.

        Returns:
            ``True`` when the coordinate lies within the maze boundaries.
        """
        x, y = cell
        return 0 <= x < self.width and 0 <= y < self.height

    def connect(self, cell: tuple[int, int], wall: Wall) -> None:
        """Remove the shared wall between two neighboring cells.

        Args:
            cell: Coordinate of the first cell.
            wall: Wall of the first cell to remove.
        """
        x, y = cell
        nx, ny = self.neighbor(cell, wall)
        opposite = {
            Wall.NORTH: Wall.SOUTH,
            Wall.EAST: Wall.WEST,
            Wall.SOUTH: Wall.NORTH,
            Wall.WEST: Wall.EAST,
        }
        self.grid[y][x] &= ~wall
        self.grid[ny][nx] &= ~opposite[wall]
