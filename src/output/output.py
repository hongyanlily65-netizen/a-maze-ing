"""Write the mandatory hexadecimal maze output."""

from src.mazegen import MazeGenerator


def write_output(maze: MazeGenerator, path: str, solution: str) -> None:
    """Write grid, endpoints and shortest path using the required format."""
    with open(path, "w", encoding="utf-8") as output_file:
        for row in maze.grid:
            output_file.write("".join(f"{cell:X}" for cell in row) + "\n")
        output_file.write("\n")
        output_file.write(f"{maze.entry[0]},{maze.entry[1]}\n")
        output_file.write(f"{maze.exit[0]},{maze.exit[1]}\n")
        output_file.write(solution + "\n")
