# https://adventofcode.com/2023/day/22

from collections import defaultdict, deque, namedtuple
from dataclasses import dataclass

Cube = namedtuple("Cube", ["x", "y", "z"])


@dataclass
class Brick:
    marker: str
    sx: int
    sy: int
    sz: int
    ex: int
    ey: int
    ez: int

    def __post_init__(self):
        assert (self.sx, self.sy, self.sz) <= (self.ex, self.ey, self.ez)
        equals = [self.sx == self.ex, self.sy == self.ey, self.sz == self.ez]
        assert equals.count(True) >= 2

    def intersect_with(self, other: "Brick") -> bool:
        return not (
            self.ex < other.sx
            or other.ex < self.sx
            or self.ey < other.sy
            or other.ey < self.sy
        )


def read_inputs(filepath):
    bricks = []
    with open(filepath) as snap:
        for i, brick in enumerate(snap.read().splitlines()):
            coords = list(map(int, brick.replace("~", ",").split(",")))
            bricks.append(Brick(str(i), *coords))
        bricks.sort(key=lambda brick: brick.sz)
        return bricks


def fall_bricks_downward(bricks: list[Brick]):
    for i in range(len(bricks)):
        new_z = 0  # How much we can fall down
        for j in range(i):
            if bricks[i].intersect_with(bricks[j]):
                new_z = max(new_z, bricks[j].ez + 1)
        bricks[i].ez -= bricks[i].sz - new_z
        bricks[i].sz = new_z

    bricks.sort(key=lambda brick: brick.sz)


def get_dependency_graph(
    bricks: list[Brick],
) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    parents = defaultdict(set)
    children = defaultdict(set)

    for i, child in enumerate(bricks):
        for j in range(i):
            parent = bricks[j]
            if child.intersect_with(parent) and child.sz - 1 == parent.ez:
                parents[child.marker].add(parent.marker)
                children[parent.marker].add(child.marker)

    return parents, children


def part1(
    bricks: list[Brick], parents: dict[str, set[str]], children: dict[str, set[str]]
) -> int:
    count = 0
    for brick in bricks:
        for child in children[brick.marker]:
            if len(parents[child]) == 1:
                break
        else:
            count += 1
    return count


def trigger_chain_reaction(
    bricks: list[Brick],
    parents: dict[str, set[str]],
    children: dict[str, set[str]],
    i: int,
):
    q = deque([bricks[i].marker])
    failling_bricks = {bricks[i].marker}

    while q:
        curr = q.popleft()
        for child in children[curr] - failling_bricks:
            # If the bricks that support this child are all failling, then fall the child.
            if all(parent in failling_bricks for parent in parents[child]):
                # Alternatively we can do set comparison as follows: parents[child] <= failling_bricks
                failling_bricks.add(child)
                q.append(child)

    return len(failling_bricks) - 1  # -1 because the brick itself is desintegrated


def part2(
    bricks: list[Brick], parents: dict[str, set[str]], children: dict[str, set[str]]
) -> int:
    return sum(
        trigger_chain_reaction(bricks, parents, children, i) for i in range(len(bricks))
    )


def main(filepath):
    bricks = read_inputs(filepath)
    fall_bricks_downward(bricks)
    parents, children = get_dependency_graph(bricks)

    print("Part 1:", part1(bricks, parents, children))
    print("Part 2:", part2(bricks, parents, children))
