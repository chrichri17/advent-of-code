# https://adventofcode.com/2023/day/19

from collections import defaultdict
from math import prod


def read_inputs(filepath):
    workflows = defaultdict(list)
    ratings = []

    with open(filepath) as file:
        wblock, rblock = file.read().strip().split("\n\n")
        for wstr in wblock.split("\n"):
            name, _, rules = wstr.strip().partition("{")
            rules = [rule.strip() for rule in rules[:-1].split(",")]
            for rule in rules:
                if ":" in rule:
                    expr, _, next_step = rule.partition(":")
                    workflows[name].append((expr, next_step))
                else:
                    workflows[name].append((None, rule))

        for rstr in rblock.splitlines():
            rstr = rstr.strip()
            rating = {
                name: int(value)
                for name, _, value in (
                    part.partition("=") for part in rstr[1:-1].split(",")
                )
            }
            ratings.append(rating)

    return workflows, ratings


def do_workflow(workflows, rating):
    step = "in"

    while step not in ("A", "R"):
        rules = workflows[step]
        for expr, next_step in rules:
            if expr is None:
                step = next_step
                break
            elif eval(expr, rating):
                step = next_step
                break
    return step == "A"


def negate(expr):
    key, op, n = expr.partition(expr[1])
    if op == "<":
        return key + ">" + str(int(n) - 1)
    else:
        return key + "<" + str(int(n) + 1)


# Use DFS to find all paths that lead to "A".
def find_all_success_paths(workflows):
    # Keeping track of the whole path is not needed. We could keep track of the last step only.
    # Doing this for debugging purposes.
    stack = [("True", ("in",))]
    paths = []

    while stack:
        expr, path = stack.pop()
        curr = path[-1]

        if curr == "A":
            paths.append((expr.removeprefix("True and "), path))
            continue
        elif curr == "R":
            continue

        rules = workflows[curr]
        curr_expr = expr

        for nexpr, next_step in rules:
            if nexpr is None:
                stack.append((curr_expr, path + (next_step,)))
            else:
                stack.append((curr_expr + " and " + nexpr, path + (next_step,)))
                # negate nexpr because at the next iteration, it would mean that we chosed the failure path.
                curr_expr = curr_expr + " and " + negate(nexpr)

    return paths


def part1(filepath):
    workflows, ratings = read_inputs(filepath)

    total = 0
    for rating in ratings:
        if do_workflow(workflows, rating):
            total += rating["x"] + rating["m"] + rating["a"] + rating["s"]

    return total


def part2(filepath):
    workflows, _ = read_inputs(filepath)
    paths = find_all_success_paths(workflows)

    total = 0

    for expr, _ in paths:
        # Use the rules to find the intervals for each variable.
        intervals = {key: (1, 4000) for key in "xmas"}
        for part in expr.split(" and "):
            key, op, n = part.partition(part[1])
            if op == "<":
                intervals[key] = (intervals[key][0], int(n) - 1)
            else:
                intervals[key] = (int(n) + 1, intervals[key][1])

        # Get the number of combinations of ratings.
        total += prod(hi - lo + 1 for lo, hi in intervals.values())

    return total


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
