# https://adventofcode.com/2024/day/14

from collections import deque

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
MOVES = dict(zip("^v<>", DIRECTIONS))
SORTER = {
    "^": lambda x: (x[0], x[1]),
    "v": lambda x: (-x[0], x[1]),
    "<": lambda x: (x[1], x[0]),
    ">": lambda x: (-x[1], x[0]),
}


class Warehouse:
    def __init__(self, data: str):
        self.grid = [list(row.strip()) for row in data.strip().splitlines()]

    @property
    def nrows(self):
        return len(self.grid)

    @property
    def ncols(self):
        return len(self.grid[0])

    @property
    def robot(self):
        return next(
            (r, c)
            for r, row in enumerate(self.grid)
            for c, cell in enumerate(row)
            if cell == "@"
        )

    @property
    def gps(self):
        return sum(
            100 * r + c
            for r, row in enumerate(self.grid)
            for c, cell in enumerate(row)
            if cell in "[O"
        )

    def expand(self):
        data = (
            str(self)
            .replace("#", "##")
            .replace("O", "[]")
            .replace(".", "..")
            .replace("@", "@.")
        )
        self.grid = [list(row) for row in data.splitlines()]

    def move(self, direction: str, robot: tuple[int, int]) -> tuple[int, int]:
        dr, dc = MOVES[direction]
        r, c = robot
        nr, nc = r + dr, c + dc

        if not (0 <= nr < self.nrows and 0 <= nc < self.ncols):
            return r, c

        # Empty space
        if self.grid[nr][nc] == ".":
            self.grid[r][c] = "."
            self.grid[nr][nc] = "@"
            return nr, nc

        # Wall
        if self.grid[nr][nc] == "#":
            return r, c

        # Move block of boxes
        boxes = self._boxes_to_move(direction, robot)
        if not boxes:
            return r, c
        for br, bc in boxes:
            self.grid[br][bc], self.grid[br + dr][bc + dc] = (
                self.grid[br + dr][bc + dc],
                self.grid[br][bc],
            )
        self.grid[r][c] = "."
        self.grid[nr][nc] = "@"
        return nr, nc

    def _boxes_to_move(self, direction: str, robot: tuple[int, int]):
        dr, dc = MOVES[direction]
        r, c = robot
        Q = deque([(r, c)])
        boxes = set()

        wall = False  # If there is a wall in the way

        while Q:
            br, bc = Q.popleft()
            if (br, bc) in boxes:
                continue
            boxes.add((br, bc))
            nr, nc = br + dr, bc + dc
            if self.grid[nr][nc] == "#":
                wall = True
                break
            if self.grid[nr][nc] == "O":
                Q.append((nr, nc))
            if self.grid[nr][nc] == "]":
                Q.append((nr, nc))
                Q.append((nr, nc - 1))
            if self.grid[nr][nc] == "[":
                Q.append((nr, nc))
                Q.append((nr, nc + 1))

        # Return sorted boxes to move so that we can move them in order
        return set() if wall else sorted(boxes, key=SORTER[direction])

    def __repr__(self):
        return "\n".join("".join(row) for row in self.grid)


def read_inputs(filepath):
    with open(filepath) as file:
        grid, moves = file.read().strip().split("\n\n")
        moves = moves.replace("\n", "")
        return Warehouse(grid), moves


def solve(filepath, expand=False):
    warehouse, moves = read_inputs(filepath)
    if expand:
        warehouse.expand()
    robot = warehouse.robot
    for move in moves:
        robot = warehouse.move(move, robot)
    return warehouse.gps


def main(filepath):
    print("Part 1:", solve(filepath))
    print("Part 2:", solve(filepath, expand=True))
