from functools import lru_cache
from typing import Iterable

# python3 brute_force.py < in.txt
# Takes around 5mn to run but works
Point = tuple[int, int]


def normalize(coords: Iterable[Point]):
    # Shift so that the minimum coordinate is (0, 0)
    mr, mc = min(r for r, _ in coords), min(c for _, c in coords)
    return tuple(sorted((r - mr, c - mc) for r, c in coords))


def print_region(W: int, H: int, mask: int):
    """Print a W×H grid, marking mask bits with #."""
    bits = f"{mask:0{W * H}b}"

    for r in range(H):
        row = ""
        for c in range(W):
            bit_index = r * W + c
            row += "#" if bits[-1 - bit_index] == "1" else "."
        print(row)
    print()


class Present:
    def __init__(self, id: int, coords: Iterable[Point]):
        self.id = id
        self.coords = normalize(coords)
        self.width = max(c for _, c in self.coords) + 1
        self.height = max(r for r, _ in self.coords) + 1

    @property
    def area(self):
        # Discrete area
        return len(self.coords)

    def __len__(self):
        return len(self.coords)

    def dihedral_group(self) -> set["Present"]:
        group = set()

        # Reflection over Y axis
        for rx in range(2):
            # Rotations: 0, 90, 180, 270 degrees
            for rot in range(4):
                coords = list(self.coords)
                for _ in range(rot):
                    # rotate clockwise
                    coords = [(c, -r) for r, c in coords]
                if rx == 1:
                    coords = [(-r, c) for r, c in coords]
                group.add(Present(self.id, coords))

        return group

    def placements_on_region(self, W: int, H: int) -> list[int]:
        if self.width > W or self.height > H:
            return []

        masks = set()
        for present in self.dihedral_group():
            # Returns bitmask for all possible placements of the present
            # on a given region with width W and height H
            for sr in range(H - self.height + 1):
                for sc in range(W - self.width + 1):
                    mask = 0
                    for r, c in present.coords:
                        idx = (r + sr) * W + (c + sc)
                        mask |= 1 << idx
                    masks.add(mask)
        return list(masks)

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, Present):
            return False
        return self.id == value.id and self.coords == value.coords

    def __hash__(self) -> int:
        return hash(tuple(self.coords))

    def __repr__(self):
        return "\n".join(
            "".join("#" if (r, c) in self.coords else "." for c in range(self.width))
            for r in range(self.height)
        )


def can_fit_region(
    W: int, H: int, counts: tuple[int, ...], presents: list[Present]
) -> bool:
    N = len(counts)
    assert N == len(presents)
    presents.sort(key=lambda p: p.id)

    total_area_needed = sum(counts[p.id] * p.area for p in presents)
    total_area_available = W * H

    if total_area_needed > total_area_available:
        return False

    placements = [p.placements_on_region(W, H) for p in presents]

    for i in range(N):
        # Fail if any present cannot fit in the region
        if counts[i] > 0 and not placements[i]:
            return False

    @lru_cache(maxsize=None)
    def count_backtrack(region: int, remaining_counts) -> bool:
        # region represents the current state. 0 means region is empty
        counts = list(remaining_counts)

        # Exit if all presents are placed
        if all(c == 0 for c in counts):
            return True

        # Exit if no more space available
        used = region.bit_count()
        free = W * H - used
        remaining_area = sum(counts[p.id] * p.area for p in presents)
        if remaining_area > free:
            return False

        best_i = None
        best_placements = None
        best_len = float("inf")

        # Find the present with the fewest possible placements
        # This allows us to prune the search space early
        for i in range(N):
            if counts[i] == 0:
                continue
            possible_placements = [
                mask for mask in placements[i] if (mask & region) == 0
            ]
            if not possible_placements:
                return False
            n = len(possible_placements)
            if n < best_len:
                best_i = i
                best_placements = possible_placements
                best_len = n
            if n == 1:
                break

        assert best_i is not None
        assert best_placements is not None

        for mask in best_placements:
            new_region = region | mask
            counts[best_i] -= 1
            if count_backtrack(new_region, tuple(counts)):
                return True
            counts[best_i] -= 1

        return False

    return count_backtrack(0, counts)


data = open(0).read()
*shapes, R = data.strip().split("\n\n")

presents = []
for shape in shapes:
    pid, *rows = shape.strip().splitlines()
    pid = pid.strip()[:-1]
    coords = [
        (r, c)
        for r, row in enumerate(rows)
        for c, char in enumerate(row.strip())
        if char == "#"
    ]
    presents.append(Present(id=int(pid), coords=coords))

total = 0
for line in R.splitlines():
    size, _, counts = line.partition(": ")
    counts = tuple(map(int, counts.split()))
    W, H = tuple(map(int, size.split("x")))

    if can_fit_region(W, H, counts, presents):
        total += 1

print(total)
