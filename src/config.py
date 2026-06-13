"""Read and validate the maze configuration file."""

from dataclasses import dataclass


@dataclass(frozen=True)
class MazeConfig:
    """Validated maze configuration."""

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: str = "0"


def _coordinate(value: str, key: str) -> tuple[int, int]:
    """Parse an x,y coordinate."""
    parts = value.split(",")
    if len(parts) != 2:
        raise ValueError(f"{key} must use the x,y format")
    try:
        return int(parts[0]), int(parts[1])
    except ValueError as error:
        raise ValueError(f"{key} must contain two integers") from error


def _boolean(value: str) -> bool:
    """Parse a strict True or False value."""
    normalized = value.lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise ValueError("PERFECT must be True or False")


def load_config(path: str) -> MazeConfig:
    """Load a configuration file and validate its values."""
    allowed = {
        "WIDTH", "HEIGHT", "ENTRY", "EXIT",
        "OUTPUT_FILE", "PERFECT", "SEED",
    }
    required = allowed - {"SEED"}
    values: dict[str, str] = {}

    with open(path, encoding="utf-8") as config_file:
        for number, raw_line in enumerate(config_file, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise ValueError(f"Invalid config syntax on line {number}")
            key, value = (part.strip() for part in line.split("=", 1))
            if key not in allowed:
                raise ValueError(f"Unknown config key: {key}")
            if key in values:
                raise ValueError(f"Duplicate config key: {key}")
            if not value and key != "SEED":
                raise ValueError(f"{key} cannot be empty")
            values[key] = value

    missing = sorted(required - values.keys())
    if missing:
        raise ValueError(f"Missing config key: {', '.join(missing)}")

    try:
        width = int(values["WIDTH"])
        height = int(values["HEIGHT"])
        seed = values.get("SEED") or "0"
        int(seed)
    except ValueError as error:
        raise ValueError("WIDTH, HEIGHT and SEED must be integers") from error

    if width < 2 or height < 2:
        raise ValueError("WIDTH and HEIGHT must be at least 2")

    entry = _coordinate(values["ENTRY"], "ENTRY")
    exit_pos = _coordinate(values["EXIT"], "EXIT")
    for name, (x, y) in (("ENTRY", entry), ("EXIT", exit_pos)):
        if not (0 <= x < width and 0 <= y < height):
            raise ValueError(f"{name} must be inside the maze")
    if entry == exit_pos:
        raise ValueError("ENTRY and EXIT must be different")

    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit=exit_pos,
        output_file=values["OUTPUT_FILE"],
        perfect=_boolean(values["PERFECT"]),
        seed=seed,
    )
