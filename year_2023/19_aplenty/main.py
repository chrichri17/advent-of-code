# https://adventofcode.com/2023/day/19

from math import prod
from typing import Union

Workflow = list[tuple[Union[str, None], str]]
Workflows = dict[str, Workflow]

Rating = dict[str, int]
Ratings = list[Rating]


def read_inputs(filepath) -> tuple[Workflows, Ratings]:
    workflows = {}
    ratings = []

    with open(filepath) as file:
        wblock, rblock = file.read().strip().split("\n\n")

        for wstr in wblock.splitlines():
            name, _, rules_str = wstr.strip()[:-1].partition("{")
            rules = rules_str.split(",")

            fallback = rules.pop()
            workflows[name] = [
                (expr, next_step)
                for expr, _, next_step in (rule.partition(":") for rule in rules)
            ]
            workflows[name].append((None, fallback))

        for rstr in rblock.splitlines():
            rstr = rstr.strip()
            rating = {
                name: int(value)
                for name, value in (part.split("=") for part in rstr[1:-1].split(","))
            }
            ratings.append(rating)

    return workflows, ratings


def accept_rating(workflows: Workflows, rating: Rating) -> bool:
    step = "in"
    while step not in ("A", "R"):
        rules = workflows[step]
        step = next(
            next_step for expr, next_step in rules if expr is None or eval(expr, rating)
        )
    return step == "A"


def negate(expr: str) -> str:
    key, op, n = expr.partition(expr[1])
    if op == "<":
        return key + ">" + str(int(n) - 1)
    else:
        return key + "<" + str(int(n) + 1)


# Use DFS to find all paths that lead to an "A".
def find_all_success_paths(workflows: Workflows) -> list[tuple[str, tuple[str]]]:
    # Keeping track of the whole path is not needed. We could keep track of the last step only.
    # Doing this for debugging purposes.
    stack = [("True", ("in",))]
    paths = []

    while stack:
        expr, path = stack.pop()
        curr = path[-1]

        if curr == "R":
            continue
        if curr == "A":
            paths.append((expr.removeprefix("True and "), path))
            continue

        rules = workflows[curr]
        curr_expr = expr

        for nexpr, next_step in rules:
            if nexpr is None:
                stack.append((curr_expr, path + (next_step,)))
                continue
            stack.append((curr_expr + " and " + nexpr, path + (next_step,)))
            # negate nexpr because at the next iteration, it would mean that we chosed the failure path.
            curr_expr = curr_expr + " and " + negate(nexpr)

    return paths


def part1(filepath) -> int:
    workflows, ratings = read_inputs(filepath)

    total = 0
    for rating in ratings:
        if accept_rating(workflows, rating):
            total += rating["x"] + rating["m"] + rating["a"] + rating["s"]

    return total


def part2(filepath) -> int:
    workflows, _ = read_inputs(filepath)
    paths = find_all_success_paths(workflows)

    total = 0

    for expr, _ in paths:
        # Use the rules to find the intervals for each variable.
        intervals = {key: (1, 4000) for key in "xmas"}
        for part in expr.split(" and "):
            key, op, n = part.partition(part[1])
            lo, hi = intervals[key]
            if op == "<":
                intervals[key] = (lo, int(n) - 1)
            else:
                intervals[key] = (int(n) + 1, hi)

        # Get the number of combinations of ratings.
        total += prod(hi - lo + 1 for lo, hi in intervals.values())

    return total


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
