"""Render a maze in the terminal."""

from src.mazegen import MazeGenerator, Wall

THEMES: list[dict[str, str]] = [
    {"wall": "\033[97m", "path": "\033[93m", "reset": "\033[0m"},
    {"wall": "\033[96m", "path": "\033[95m", "reset": "\033[0m"},
    {"wall": "\033[92m", "path": "\033[94m", "reset": "\033[0m"},
]


def render_ascii(
    maze: MazeGenerator,
    path: list[tuple[int, int]],
    show_path: bool,
    theme: dict[str, str],
) -> None:
    """Print a colored ASCII representation of a maze.

    Args:
        maze: Generated maze to render.
        path: Coordinates of the solution path.
        show_path: Whether to display the solution path.
        theme: ANSI colors for walls, the path, and resetting output.
    """
    wall = theme["wall"]
    path_color = theme["path"]
    reset = theme["reset"]
    path_cells = set(path) if show_path else set()

    for y, row in enumerate(maze.grid):
        top = []
        middle = []
        for x, cell in enumerate(row):
            top.append(wall + "+" + ("---" if cell & Wall.NORTH else "   "))
            middle.append(wall + ("|" if cell & Wall.WEST else " ") + reset)
            position = (x, y)
            if position == maze.entry:
                symbol = "\033[92m E "
            elif position == maze.exit:
                symbol = "\033[91m X "
            elif position in maze.pattern42:
                symbol = "\033[95m###"
            elif position in path_cells:
                symbol = path_color + "***"
            else:
                symbol = "   "
            middle.append(symbol + reset)
        print("".join(top) + wall + "+" + reset)
        east = "|" if row[-1] & Wall.EAST else " "
        print("".join(middle) + wall + east + reset)
    print(wall + "+---" * maze.width + "+" + reset)
