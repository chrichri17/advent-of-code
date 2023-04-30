from dataclasses import dataclass
from itertools import cycle

Shape = tuple[int, int]

# NOTE: we can use complex numbers instead
ROCKS = [
    ((0, 0), (1, 0), (2, 0), (3, 0)),  # minus shape
    ((1, 0), (0, 1), (1, 1), (2, 1), (1, 2)),  # plus shape
    ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)),  # reversed L shape
    ((0, 0), (0, 1), (0, 2), (0, 3)),  # | shape
    ((0, 0), (1, 0), (0, 1), (1, 1)),  # square shape
]


WIDTH = 7
FLOOR = -1
PADX = 2
PADY = 3


@dataclass
class Rock:
    shapes: list[tuple[int, int]]

    def init(self, ymax: int = -1):
        for i, shape in enumerate(self):
            self[i] = shape[0] + PADX, shape[1] + PADY + ymax + 1

    def move(self, gas_push: str, occupied: set[Shape]) -> bool:
        if gas_push == "<":
            self.move_left(occupied)
        else:
            self.move_right(occupied)
        return self.move_down(occupied)

    def move_left(self, occupied: set[Shape]) -> bool:
        for x, y in self:
            if x == 0 or (x - 1, y) in occupied:
                return False

        self.shapes = list(map(lambda shape: (shape[0] - 1, shape[1]), self))
        return True

    def move_right(self, occupied: set[Shape]) -> bool:
        for x, y in self:
            if x == WIDTH - 1 or (x + 1, y) in occupied:
                return False

        self.shapes = list(map(lambda shape: (shape[0] + 1, shape[1]), self))
        return True

    def move_down(self, occupied: set[Shape]) -> bool:
        for x, y in self:
            if y == 0 or (x, y - 1) in occupied:
                return False

        self.shapes = list(map(lambda shape: (shape[0], shape[1] - 1), self))
        return True

    def __getitem__(self, i: int):
        return self.shapes[i]

    def __setitem__(self, i: int, shape: Shape):
        self.shapes[i] = shape

    def __iter__(self):
        return iter(self.shapes)


def get_jets(filepath) -> list[str]:
    with open(filepath) as file:
        return list(file.readline().strip())


def signature(occupied: set[Shape], ymax: int, nb_rows: int = 20):
    return frozenset((x, ymax - y) for (x, y) in occupied if ymax - y <= nb_rows)


def get_tower_height(max_rocks: int, jets: list[str]) -> int:
    n = len(jets)
    rocks = cycle(ROCKS)
    jets = cycle(enumerate(jets))
    occupied: set[Shape] = set()
    ymax = -1
    offset = 0
    cache = {}
    rock_count = 0

    while rock_count < max_rocks:
        rock = Rock(list(next(rocks)))
        rock.init(ymax)
        moved = True

        while moved:
            jet_idx, jet = next(jets)
            moved = rock.move(jet, occupied)

        occupied |= set(rock)
        ymax = max(ymax, *(y for _, y in rock))

        # Use the cache to skip iterations when a cycle is detected.
        #
        # It turns out it works pretty well wif we consider only
        # the last 5 rows: `nb_rows=5`
        sign = (jet_idx % n, rock_count % 5, signature(occupied, ymax, 5))
        if sign in cache:
            lrc, ly = cache[sign]  # get last values
            dt = rock_count - lrc
            dy = ymax - ly
            # skip a bunch of repetition
            nb_cycle = (max_rocks - rock_count) // dt
            offset += nb_cycle * dy
            rock_count += nb_cycle * dt
            # reset the cache
            cache = {}
        cache[sign] = (rock_count, ymax)

        rock_count += 1

    return ymax + 1 + offset


def main(filepath):
    jets = get_jets(filepath)
    print("Part 1:", get_tower_height(2022, jets))
    # To speed up, we need to find a repetition pattern
    # This means that we can check for cycles while building
    # the tower. If we already explored a state, we can skip
    # the next coming cycles and assume that the result will be
    # the height difference times the number of cycles left.
    print("Part 2:", get_tower_height(1_000_000_000_000, jets))
