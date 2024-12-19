# https://adventofcode.com/2021/day/13

import re
from dataclasses import dataclass


@dataclass
class TransparentPaper:
    dots: set[tuple[int, int]]

    def __repr__(self):
        width = max(x for x, _ in self.dots) + 1
        height = max(y for _, y in self.dots) + 1

        rows = [""]
        for y in range(height):
            rows.append(
                "".join("##" if (x, y) in self.dots else "  " for x in range(width))
            )
        return "\n".join(rows)


@dataclass
class Folder:
    axis: str
    pos: int

    def __post_init__(self):
        assert self.axis in "xy"

    def fold(self, paper: TransparentPaper):
        if self.axis == "x":
            return self._vertical_fold(paper)
        return self._horizontal_fold(paper)

    def _horizontal_fold(self, paper: TransparentPaper):
        fy = self.pos
        new_dots = set()
        for x, y in paper.dots:
            if y < fy:
                new_dots.add((x, y))
            else:
                new_dots.add((x, fy - (y - fy)))
        return TransparentPaper(new_dots)

    def _vertical_fold(self, paper: TransparentPaper):
        fx = self.pos
        new_dots = set()
        for x, y in paper.dots:
            if x < fx:
                new_dots.add((x, y))
            else:
                new_dots.add((fx - (x - fx), y))
        return TransparentPaper(new_dots)


def read_inputs(filepath):
    with open(filepath) as file:
        dots, instructions = file.read().split("\n\n")
        dots = set(
            tuple(map(int, line.split(","))) for line in dots.strip().splitlines()
        )
        folders = [
            Folder(axis, pos=int(pos))
            for axis, pos in re.findall(r"(x|y)=(\d+)", instructions)
        ]
        return TransparentPaper(dots), folders


def part1(filepath):
    paper, folders = read_inputs(filepath)
    paper = folders[0].fold(paper)
    return len(paper.dots)


def part2(filepath):
    paper, folders = read_inputs(filepath)
    for folder in folders:
        paper = folder.fold(paper)
    return paper


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
