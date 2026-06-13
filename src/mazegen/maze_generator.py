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
    """Generate a maze with randomized Prim's algorithm."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_pos: tuple[int, int],
        perfect: bool = True,
        seed: str = "0",
    ) -> None:
        """Store generation settings."""
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit_pos
        self.perfect = perfect
        self.seed = seed
        self.grid: list[list[int]] = []
        self.pattern42: set[tuple[int, int]] = set()

    def generate(self) -> list[list[int]]:
        """Create and return a new maze."""
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
        """Return the neighboring coordinate in one direction."""
        x, y = cell
        moves = {
            Wall.NORTH: (x, y - 1),
            Wall.EAST: (x + 1, y),
            Wall.SOUTH: (x, y + 1),
            Wall.WEST: (x - 1, y),
        }
        return moves[wall]

    def inside(self, cell: tuple[int, int]) -> bool:
        """Return whether a coordinate is inside the maze."""
        x, y = cell
        return 0 <= x < self.width and 0 <= y < self.height

    def connect(self, cell: tuple[int, int], wall: Wall) -> None:
        """Remove matching walls between two neighboring cells."""
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
