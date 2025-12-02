# https://adventofcode.com/2021/day/7


def read_inputs(filepath):
    with open(filepath) as file:
        return list(map(int, file.read().strip().split(",")))


def fuel_amount(positions, cost_fn):
    m, M = min(positions), max(positions)
    cheapest = float("inf")
    for pos in range(m, M + 1):
        cost = sum(cost_fn(pos, p) for p in positions)
        cheapest = min(cheapest, cost)
    return cheapest


def part1(filepath):
    positions = read_inputs(filepath)
    return fuel_amount(positions, cost_fn=lambda x, y: abs(x - y))


def part2(filepath):
    positions = read_inputs(filepath)

    def cost_fn(x, y):
        n = abs(x - y)
        return (n * (n + 1)) // 2

    return fuel_amount(positions, cost_fn)


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
