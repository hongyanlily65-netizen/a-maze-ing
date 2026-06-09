"""Find the shortest maze path with breadth-first search."""

from collections import deque
from typing import Optional

from .maze_generator import MazeGenerator, Wall


def solve_shortest(maze: MazeGenerator) -> list[tuple[int, int]]:
    """Return the shortest path from entry to exit."""
    queue = deque([maze.entry])
    parent: dict[
        tuple[int, int], Optional[tuple[int, int]]
    ] = {maze.entry: None}

    while queue:
        cell = queue.popleft()
        if cell == maze.exit:
            break
        x, y = cell
        for wall in Wall:
            next_cell = maze.neighbor(cell, wall)
            if (
                maze.inside(next_cell)
                and not maze.grid[y][x] & wall
                and next_cell not in parent
            ):
                parent[next_cell] = cell
                queue.append(next_cell)

    if maze.exit not in parent:
        return []
    path = []
    current: Optional[tuple[int, int]] = maze.exit
    while current is not None:
        path.append(current)
        current = parent[current]
    return path[::-1]


def directions(path: list[tuple[int, int]]) -> str:
    """Convert a coordinate path to N, E, S and W letters."""
    result = []
    for (x, y), (next_x, next_y) in zip(path, path[1:]):
        if next_y < y:
            result.append("N")
        elif next_x > x:
            result.append("E")
        elif next_y > y:
            result.append("S")
        else:
            result.append("W")
    return "".join(result)
