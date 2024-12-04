from typing import Generator

## Directions in a square grid
DIRECTIONS = [
    # Horizontal
    (0, 1),
    (0, -1),
    # Vertical
    (1, 0),
    (-1, 0),
    # Diagonal x + y = cte
    (1, 1),
    (-1, -1),
    # Diagonal x - y = cte
    (1, -1),
    (-1, 1),
]

Position = tuple[int, int]
# Direction = "L" | "R" | "U" | "D" | "UL" | "UR" | "DL" | "DR"


def normalize_direction(direction: str) -> str:
    mapping = {"N": "U", "S": "D", "E": "R", "W": "L"}
    return "".join(map(lambda x: mapping.get(x, x), direction))


def move(direction: str, pos: Position, n: int = 1) -> Generator[Position, None, None]:
    direction = normalize_direction(direction)
    dr, dc = 0, 0
    if direction == "L":
        dr, dc = 0, -1
    elif direction == "R":
        dr, dc = 0, 1
    elif direction == "U":
        dr, dc = -1, 0
    elif direction == "D":
        dr, dc = 1, 0
    elif direction == "DR":
        dr, dc = 1, 1
    elif direction == "DL":
        dr, dc = 1, -1
    elif direction == "UR":
        dr, dc = -1, 1
    elif direction == "UL":
        dr, dc = -1, -1
    else:
        raise ValueError(f"Invalid direction: {direction}")
    r, c = pos
    for i in range(1, n + 1):
        yield (r + i * dr, c + i * dc)


def corners(pos: Position) -> Generator[Position, None, None]:
    return [next(move(direction, pos)) for direction in ["UL", "UR", "DL", "DR"]]
