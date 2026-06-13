"""Place the required closed-cell 42 pattern."""

from collections import deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .maze_generator import MazeGenerator


PATTERN = {
    (0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1), (2, 2),
    (2, 3), (2, 4), (4, 0), (5, 0), (6, 0), (6, 1), (4, 2),
    (5, 2), (6, 2), (4, 3), (4, 4), (5, 4), (6, 4),
}


def add_42_pattern(maze: "MazeGenerator") -> set[tuple[int, int]]:
    """Find a valid center-first location for the closed-cell 42 pattern.

    Args:
        maze: Maze in which to position the pattern.

    Returns:
        Coordinates occupied by the pattern, or an empty set when no valid
        position exists.
    """
    if maze.width < 9 or maze.height < 7:
        print("Warning: maze is too small to contain the 42 pattern.")
        return set()

    center_x = (maze.width - 7) // 2
    center_y = (maze.height - 5) // 2
    origins = [
        (x, y)
        for y in range(maze.height - 5 + 1)
        for x in range(maze.width - 7 + 1)
    ]
    origins.sort(
        key=lambda origin: (
            abs(origin[0] - center_x) + abs(origin[1] - center_y),
            origin[1],
            origin[0],
        )
    )
    for origin_x, origin_y in origins:
        pattern = {
            (origin_x + x, origin_y + y) for x, y in PATTERN
        }
        if (
            maze.entry not in pattern
            and maze.exit not in pattern
            and _remaining_cells_connected(maze, pattern)
        ):
            return pattern

    print("Warning: no valid position was found for the 42 pattern.")
    return set()


def _remaining_cells_connected(
    maze: "MazeGenerator", pattern: set[tuple[int, int]]
) -> bool:
    """Check whether all cells outside a proposed pattern remain connected.

    Args:
        maze: Maze whose dimensions and endpoints are checked.
        pattern: Proposed set of closed pattern coordinates.

    Returns:
        ``True`` if every non-pattern cell is reachable from the entry.
    """
    available = {
        (x, y)
        for y in range(maze.height)
        for x in range(maze.width)
        if (x, y) not in pattern
    }
    if maze.entry not in available or maze.exit not in available:
        return False

    visited = {maze.entry}
    queue = deque([maze.entry])
    while queue:
        x, y = queue.popleft()
        for neighbor in ((x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)):
            if neighbor in available and neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return visited == available
