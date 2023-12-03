# https://adventofcode.com/2023/day/3

import re
from collections import defaultdict
from dataclasses import dataclass
from math import prod
from typing import Generator

EngineSchematic = list[list[str]]


@dataclass
class Number:
    pos: tuple[int, int]
    raw: str

    @property
    def value(self) -> int:
        return int(self.raw)

    def is_part_number(self, schematic: EngineSchematic) -> bool:
        symbols = self.get_adjacent_symbols(schematic)
        try:
            next(symbols)
            return True
        except StopIteration:
            return False

    def get_adjacent_stars(
        self, schematic: EngineSchematic
    ) -> Generator[tuple[int, int], None, None]:
        for x, y, symbol in self.get_adjacent_symbols(schematic):
            if symbol == "*":
                yield (x, y)

    def get_adjacent_symbols(
        self, schematic: EngineSchematic
    ) -> Generator[tuple[int, int, str], None, None]:
        """Returns adjacent symbols to the number in the schematic:

        Example: for number 633 in the schematic below, the only symbol is #
        .....
        .633.
        .#...
        """
        i, j = self.pos
        for x in range(i - 1, i + 2):
            for y in range(j - 1, j + len(self) + 1):
                # We can skip for x == i and j <= y < j + len(num)
                # but it's not worth it
                try:
                    symbol = schematic[x][y]
                    if symbol != "." or not symbol.isdigit():
                        yield (x, y, symbol)
                except IndexError:
                    continue

    def __hash__(self) -> int:
        return hash((self.pos, self.raw))

    def __len__(self) -> int:
        return len(self.raw)


def read_inputs(filepath) -> tuple[EngineSchematic, set[Number]]:
    schematic: EngineSchematic = []
    numbers: set[Number] = set()

    with open(filepath) as file:
        for i, line in enumerate(file.readlines()):
            # Numbers from this string "467..467.."  are ((i, 0), 467), ((i, 3), 467)
            line = line.strip()
            pattern = r"\d+"
            for match in re.finditer(pattern, line):
                numbers.add(Number(pos=(i, match.start()), raw=match.group()))
            schematic.append(list(line))

    return schematic, numbers


def part_numbers_sum(filepath):
    schematic, numbers = read_inputs(filepath)
    return sum(number.value for number in numbers if number.is_part_number(schematic))


def gear_ratios_sum(filepath):
    schematic, numbers = read_inputs(filepath)

    gears = defaultdict(list)
    for number in numbers:
        for x, y in number.get_adjacent_stars(schematic):
            gears[(x, y)].append(number.value)

    return sum(prod(nums) for nums in gears.values() if len(nums) == 2)


def main(filepath):
    print("Part 1:", part_numbers_sum(filepath))
    print("Part 2:", gear_ratios_sum(filepath))
