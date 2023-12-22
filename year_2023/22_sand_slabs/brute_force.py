from collections import defaultdict, deque, namedtuple
from copy import deepcopy
from dataclasses import dataclass, field

Brick = namedtuple("Brick", ["x", "y", "z"])

D3_SPACE = set()


@dataclass
class Line:
    name: str
    start: Brick
    end: Brick
    bricks: list[Brick] = field(default_factory=list)

    def __post_init__(self):
        assert self.start <= self.end
        self.bricks = []
        s, e = self.start, self.end

        if s.x == e.x and s.y == e.y:
            for z in range(s.z, e.z + 1):
                self.bricks.append(Brick(s.x, s.y, z))
        elif s.x == e.x and s.z == e.z:
            for y in range(s.y, e.y + 1):
                self.bricks.append(Brick(s.x, y, s.z))
        elif s.y == e.y and s.z == e.z:
            for x in range(s.x, e.x + 1):
                self.bricks.append(Brick(x, s.y, s.z))
        else:
            assert False

    def can_move_down(self, d3_space):
        for brick in self.bricks:
            if brick.z == 1:
                return False
            if (brick.x, brick.y, brick.z - 1) in d3_space and (
                brick.x,
                brick.y,
                brick.z - 1,
            ) not in self.bricks:
                return False
        return True

    def fall_deep_down(self, d3_space):
        while self.can_move_down(d3_space):
            for i, brick in enumerate(self.bricks):
                d3_space.remove(brick)
                self.bricks[i] = Brick(brick.x, brick.y, brick.z - 1)
                d3_space.add(self.bricks[i])
            self.start = self.bricks[0]
            self.end = self.bricks[-1]


def overlaps(a, b):
    return not (
        a.end.x < b.start.x
        or b.end.x < a.start.x
        or a.end.y < b.start.y
        or b.end.y < a.start.y
    )
    # return max(a.start.x, b.start.x) <= min(a.end.x, b.end.x) and max(
    #     a.start.y, b.start.y
    # ) <= min(a.end.y, b.end.y)


def read_inputs(filepath):
    lines = []
    d3_space = set()
    with open(filepath) as file:
        for i, line in enumerate(file.read().splitlines()):
            left, right = line.strip().split("~")
            sx, sy, sz = [int(i) for i in left.split(",")]
            ex, ey, ez = [int(i) for i in right.split(",")]
            lines.append(
                Line(
                    name=str(i),
                    start=Brick(sx, sy, sz),
                    end=Brick(ex, ey, ez),
                )
            )
            for brick in lines[-1].bricks:
                d3_space.add(brick)

        lines.sort(key=lambda line: line.start.z)

        return lines, d3_space


def settle_bricks(lines, d3_space):
    for line in lines:
        line.fall_deep_down(d3_space)

    # Dependency graph: parent -> child means parent supports child
    parents = defaultdict(set)
    children = defaultdict(set)

    for i, child in enumerate(lines):
        # Find the parent lines that is supported by this child
        for j, parent in enumerate(lines[:i]):
            if i == j:
                continue
            if overlaps(parent, child) and child.start.z - 1 == parent.end.z:
                parents[child.name].add(parent.name)
                children[parent.name].add(child.name)

    return parents, children


def part1(lines, parents, children):
    count = 0
    for line in lines:
        for child in children[line.name]:
            if len(parents[child]) == 1:
                break
        else:
            count += 1
    return count


def trigger_chain_reaction(parents, children, line):
    q = deque([line.name])
    count = 0

    while q:
        curr = q.popleft()
        for child in list(children[curr]):
            parents[child].remove(curr)
            children[curr].remove(child)
            if len(parents[child]) == 0:
                count += 1
                q.append(child)

    return count


def part2(lines, parents, children):
    return sum(
        trigger_chain_reaction(deepcopy(parents), deepcopy(children), line)
        for line in lines
    )


def main(filepath):
    lines, d3_space = read_inputs(filepath)
    parents, children = settle_bricks(lines, d3_space)
    print("Part 1:", part1(lines, parents, children))
    print("Part 2:", part2(lines, parents, children))
