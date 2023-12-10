from collections import deque


def read_inputs(filepath):
    maze = []
    with open(filepath) as file:
        maze = [list(line.strip()) for line in file.readlines()]

    # Find the starting point
    for r, row in enumerate(maze):
        for c, tile in enumerate(row):
            if tile == "S":
                sr, sc = r, c
                break
        else:
            # Happens if the inner loop doesn't break
            continue
        # Happens if the inner loop does
        break

    # Find the main loop
    loop = find_main_loop(maze, sr, sc)

    ## Replace the junk values with dots
    maze = [
        [tile if (r, c) in loop else "." for c, tile in enumerate(row)]
        for r, row in enumerate(maze)
    ]

    return maze, loop


# Find connected component of the starting point
def find_main_loop(maze, sr: int, sc: int):
    nrows, ncols = len(maze), len(maze[0])
    loop = {(sr, sc)}
    queue = deque([(sr, sc)])
    maybe_s = {"L", "J", "7", "F", "|", "-"}

    while queue:
        r, c = queue.popleft()
        tile = maze[r][c]

        # Go up
        if (
            r > 0
            and tile in "S|JL"
            and maze[r - 1][c] in "|F7"
            and (r - 1, c) not in loop
        ):
            loop.add((r - 1, c))
            queue.append((r - 1, c))
            if tile == "S":
                maybe_s &= {"|", "J", "L"}

        # Go down
        if (
            r < nrows - 1
            and tile in "S|F7"
            and maze[r + 1][c] in "|JL"
            and (r + 1, c) not in loop
        ):
            loop.add((r + 1, c))
            queue.append((r + 1, c))
            if tile == "S":
                maybe_s &= {"|", "F", "7"}

        # Go left
        if (
            c > 0
            and tile in "S-7J"
            and maze[r][c - 1] in "-LF"
            and (r, c - 1) not in loop
        ):
            loop.add((r, c - 1))
            queue.append((r, c - 1))
            if tile == "S":
                maybe_s &= {"-", "J", "7"}

        # Go right
        if (
            c < ncols - 1
            and tile in "S-LF"
            and maze[r][c + 1] in "-7J"
            and (r, c + 1) not in loop
        ):
            loop.add((r, c + 1))
            queue.append((r, c + 1))
            if tile == "S":
                maybe_s &= {"-", "F", "L"}

    ## Infer the starting tile and replace it in the maze
    assert len(maybe_s) == 1
    maze[sr][sc] = maybe_s.pop()

    return loop


def part1(filepath):
    _, loop = read_inputs(filepath)
    return len(loop) // 2


# Damn this is hard ! Credits to @hyper-neutrino for the simpler solution.
#
# Solution: For each line, find the characters inside the pipeline by counting the number of times it crosses the pipeline.
#
# A character is inside the pipeline if the number of times it crosses the pipeline is odd in all four directions
# Here are the possible limits of the pipeline we can encounter vertically:
#   LJ or L-J or L-J ...
#   F7 or F-7 or F-7 ...
#   L7 or L-7 or L-7 ...
#   FJ or F-J or F-J ...
#   ||
#
# The trick here is to not consider some special cases. Since squeezing between pipes is also allowed:
#   - We can escape the pipeline for situations like: LJ or F7
#   - We will cross the pipeline for situations like: L7 or FJ
def part2(filepath):
    maze, _ = read_inputs(filepath)
    inside = set()

    for r, row in enumerate(maze):
        is_inside = False
        curr_limit = None  # Can be LJ, etc.

        for c, tile in enumerate(row):
            if tile == "|":
                assert curr_limit is None
                is_inside = not is_inside
            elif tile == "-":
                assert curr_limit is not None
                curr_limit += tile
            elif tile in "LF":
                assert curr_limit is None
                curr_limit = tile
            elif tile in "7J":
                assert curr_limit is not None
                if (curr_limit[0] + tile) in {"L7", "FJ"}:
                    is_inside = not is_inside
                curr_limit = None
            elif tile == ".":
                if is_inside:
                    inside.add((r, c))
            else:
                raise ValueError(f"Invalid inputs: unexpected tile: {tile}")
    return len(inside)


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
