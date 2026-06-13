"""Write the mandatory hexadecimal maze output."""

from src.mazegen import MazeGenerator


def write_output(maze: MazeGenerator, path: str, solution: str) -> None:
    """Write a maze and its solution using the required output format.

    Args:
        maze: Generated maze to serialize.
        path: Destination file path.
        solution: Shortest path encoded as cardinal direction letters.

    Raises:
        OSError: If the destination file cannot be written.
    """
    with open(path, "w", encoding="utf-8") as output_file:
        for row in maze.grid:
            output_file.write("".join(f"{cell:X}" for cell in row) + "\n")
        output_file.write("\n")
        output_file.write(f"{maze.entry[0]},{maze.entry[1]}\n")
        output_file.write(f"{maze.exit[0]},{maze.exit[1]}\n")
        output_file.write(solution + "\n")
