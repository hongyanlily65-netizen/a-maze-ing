#!/usr/bin/env python3
"""A-Maze-ing command-line application."""

import os
import sys

from src.config import load_config
from src.mazegen import MazeGenerator, directions, solve_shortest
from src.output import write_output
from src.render import THEMES, render_ascii


def clear_screen() -> None:
    """Clear an interactive terminal."""
    if sys.stdout.isatty():
        os.system("clear")


def generate_maze(
    maze: MazeGenerator, output_file: str
) -> list[tuple[int, int]]:
    """Generate, solve, and write a maze."""
    maze.generate()
    path = solve_shortest(maze)
    if not path:
        raise ValueError("No path exists between ENTRY and EXIT")
    write_output(maze, output_file, directions(path))
    return path


def main() -> int:
    """Load, generate, render and interact with a maze."""
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} config.txt", file=sys.stderr)
        return 1
    try:
        config = load_config(sys.argv[1])
        maze = MazeGenerator(
            config.width,
            config.height,
            config.entry,
            config.exit,
            config.perfect,
            config.seed,
        )
        path = generate_maze(maze, config.output_file)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    show_path = False
    theme_index = 0
    while True:
        clear_screen()
        render_ascii(maze, path, show_path, THEMES[theme_index])
        path_status = "Shown" if show_path else "Hidden"
        print(f"\nPath: {path_status}")
        print("1. New maze")
        print("2. Show/Hide path")
        print("3. Change colour")
        print("4. Exit")
        try:
            choice = input("\nSelect an option: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if choice == "1":
            try:
                maze.seed = None
                path = generate_maze(maze, config.output_file)
                show_path = False
            except (OSError, ValueError) as error:
                print(f"Error: {error}", file=sys.stderr)
                return 1
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            theme_index = (theme_index + 1) % len(THEMES)
        elif choice == "4":
            return 0
        else:
            input("Invalid option. Press Enter to continue.")


if __name__ == "__main__":
    raise SystemExit(main())
