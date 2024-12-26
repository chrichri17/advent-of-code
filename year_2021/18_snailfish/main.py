# https://adventofcode.com/2021/day/18

import math
from dataclasses import dataclass


@dataclass
class RegularNumber:
    value: int
    depth: int

    def copy(self):
        return RegularNumber(self.value, self.depth)


@dataclass
class Snailfish:
    nums: list[RegularNumber]

    def __add__(self, other: "Snailfish"):
        return Snailfish(
            nums=[RegularNumber(x.value, x.depth + 1) for x in self.nums + other.nums]
        )

    @property
    def magnitude(self):
        Q = []

        for num in self.nums:
            Q.append(num.copy())

            while len(Q) > 1 and Q[-1].depth == Q[-2].depth:
                Q[-2].value = 3 * Q[-2].value + 2 * Q[-1].value
                Q[-2].depth -= 1
                Q.pop()

        return Q[0].value

    def reduce(self):
        changed = True
        while changed:
            changed = self.reduce_once()
        return self

    def reduce_once(self):
        # First action: explode leftmost pairs of depth 4
        if self._explode_leftmost_pair_depth4():
            return True
        # Second action: split leftmost regular number greater than 10
        return self._split_leftmost_regular_number_gt10()

    def _explode_leftmost_pair_depth4(self):
        for i, num in enumerate(self.nums):
            if num.depth != 4:
                continue
            assert i + 1 < len(self.nums)
            assert self.nums[i + 1].depth == 4, self.nums[i : i + 2]
            # leftmost regular number
            left = self.nums[i - 1] if i > 0 else None
            # rightmost regular number
            right = self.nums[i + 2] if i + 2 < len(self.nums) else None

            if left:
                left.value += num.value
            if right:
                right.value += self.nums[i + 1].value

            # replace the pair by 0
            num.value = 0
            num.depth -= 1
            self.nums.pop(i + 1)
            return True

        return False

    def _split_leftmost_regular_number_gt10(self):
        for i, num in enumerate(self.nums):
            if num.value < 10:
                continue
            lo, hi = math.floor(num.value / 2), math.ceil(num.value / 2)
            num.value = lo
            num.depth += 1
            self.nums.insert(i + 1, RegularNumber(hi, num.depth))
            return True

        return False


def read_inputs(filepath) -> list[Snailfish]:
    def read_snailfish(data: str) -> Snailfish:
        # Read the snailfish numbers as a single flattened list of RegularNumber
        depth = -1
        nums = []
        for c in data:
            if c == "[":
                depth += 1
            elif c == "]":
                depth -= 1
            elif c.isdigit():
                nums.append(RegularNumber(int(c), depth))
        return Snailfish(nums)

    with open(filepath) as f:
        return list(map(read_snailfish, f.read().splitlines()))


def part1(filepath):
    snailfishes = read_inputs(filepath)
    curr = snailfishes[0]
    for i in range(1, len(snailfishes)):
        curr += snailfishes[i]
        curr = curr.reduce()
    return curr.magnitude


def part2(filepath):
    snailfishes = read_inputs(filepath)
    largest = 0

    for i, x in enumerate(snailfishes):
        for y in snailfishes[i + 1 :]:
            largest = max(largest, (x + y).reduce().magnitude)
            largest = max(largest, (y + x).reduce().magnitude)

    return largest


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
