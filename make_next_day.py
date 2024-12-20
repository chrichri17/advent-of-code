import argparse
from pathlib import Path

import utils


def parse_args():
    parser = argparse.ArgumentParser()
    last_year = utils.get_last_year()

    parser.add_argument("name")
    parser.add_argument("-y", "--year", default=last_year)
    parser.add_argument("-d", "--day", default="")

    args = parser.parse_args()
    if not args.day:
        last_day = int(utils.get_last_day(args.year))
        args.day = f"{last_day + 1:02d}"
    return args


files = [
    "main.py",
    "data/in.txt",
    "data/test.txt",
    "data/out.txt",
]

boilerplate = """
# https://adventofcode.com/{year}/day/{day}

import heapq
import re
from collections import Counter, defaultdict, deque
from math import gcd, lcm, prod


def read_inputs(filepath):
    with open(filepath) as file:
        for line in file.readlines():
            yield line.strip()


def part1(filepath):
    pass


def part2(filepath):
    pass


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
"""


def main():
    args = parse_args()
    cleaned_name = args.name.replace(" ", "_")

    module_name = f"{args.day}_{cleaned_name}"
    base_dir = Path(f"year_{args.year}") / module_name

    for filename in files:
        p = base_dir / filename
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch()

    with open(base_dir / "main.py", "w") as main_file:
        main_file.write(boilerplate.format(year=args.year, day=args.day))


if __name__ == "__main__":
    main()
