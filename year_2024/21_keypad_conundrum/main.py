# https://adventofcode.com/2024/day/21

import math
from collections import deque
from functools import cache
from itertools import product

num_keypad = (
    ("7", "8", "9"),
    ("4", "5", "6"),
    ("1", "2", "3"),
    (None, "0", "A"),
)

dir_keypad = (
    (None, "^", "A"),
    ("<", "v", ">"),
)


@cache
def shortest_paths(keypad, source, target):
    """
    Find all the shortest paths from source to target on the keypad
    """
    nrows, ncols = len(keypad), len(keypad[0])
    sr, sc = next(
        (r, c) for r in range(nrows) for c in range(ncols) if keypad[r][c] == source
    )
    Q = deque([(sr, sc, "")])
    best_length = math.inf
    paths = []

    while Q:
        r, c, path = Q.popleft()
        if keypad[r][c] == target:
            if best_length < len(path):
                break
            best_length = len(path)
            paths.append(path + "A")

        for dr, dc, d in [(0, 1, ">"), (0, -1, "<"), (1, 0, "v"), (-1, 0, "^")]:
            nr, nc = r + dr, c + dc
            if nr < 0 or nc < 0 or nr >= nrows or nc >= ncols:
                continue
            if keypad[nr][nc] is None:
                continue
            Q.append((nr, nc, path + d))

    return paths


def shortest_sequences(keypad, code):
    # Cartesian product of all shortest paths between each pair
    # of consecutive char in the code (starting from A)
    paths = [
        shortest_paths(keypad, source, target)
        for source, target in zip("A" + code, code)
    ]
    return set("".join(seq) for seq in product(*paths))


@cache
def shortest_dir_length(subseq, depth=25):
    if depth == 1:
        return sum(
            len(shortest_paths(dir_keypad, s, t)[0])
            for s, t in zip("A" + subseq, subseq)
        )

    length = 0
    for s, t in zip("A" + subseq, subseq):
        # For each pair (s, t), find the minimum length of moves required
        # by ronot depth - 1, to go from s to t
        length += min(
            shortest_dir_length(subseq, depth - 1)
            for subseq in shortest_paths(dir_keypad, s, t)
        )
    return length


def read_inputs(filepath):
    with open(filepath) as file:
        for line in file.readlines():
            yield line.strip()


def solve(codes, nb_dir_robots=2):
    fn = lambda x: shortest_dir_length(x, nb_dir_robots)
    total = 0
    for code in codes:
        robot1 = shortest_sequences(num_keypad, code)
        shortest_length = min(map(fn, robot1))
        total += shortest_length * int(code[:-1])
    return total


def main(filepath):
    codes = list(read_inputs(filepath))
    print("Part 1:", solve(codes))
    print("Part 2:", solve(codes, 25))
