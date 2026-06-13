"""Randomized Prim maze generation."""

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .maze_generator import MazeGenerator


def generate_prim(maze: "MazeGenerator") -> None:
    """Carve a connected maze while leaving the 42 cells closed."""
    from .maze_generator import Wall

    available = {
        (x, y)
        for y in range(maze.height)
        for x in range(maze.width)
        if (x, y) not in maze.pattern42
    }
    start = maze.entry
    if start not in available:
        raise ValueError("The 42 pattern overlaps the entry")

    visited = {start}
    frontier = [(start, wall) for wall in Wall]
    while frontier:
        index = random.randrange(len(frontier))
        cell, wall = frontier.pop(index)
        next_cell = maze.neighbor(cell, wall)
        if next_cell not in available or next_cell in visited:
            continue
        maze.connect(cell, wall)
        visited.add(next_cell)
        frontier.extend((next_cell, direction) for direction in Wall)

    if visited != available:
        raise ValueError(
            "The 42 pattern splits the maze into disconnected areas"
        )
    if not maze.perfect:
        _add_loop(maze)


def _add_loop(maze: "MazeGenerator") -> None:
    """Remove one extra internal wall to make the maze imperfect."""
    from .maze_generator import Wall

    candidates = [
        ((x, y), wall)
        for y in range(maze.height)
        for x in range(maze.width)
        for wall in (Wall.EAST, Wall.SOUTH)
        if (x, y) not in maze.pattern42
        and maze.inside(maze.neighbor((x, y), wall))
        and maze.neighbor((x, y), wall) not in maze.pattern42
        and maze.grid[y][x] & wall
    ]
    random.shuffle(candidates)
    if candidates:
        maze.connect(*candidates[0])
