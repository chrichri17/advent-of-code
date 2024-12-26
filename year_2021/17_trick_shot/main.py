# https://adventofcode.com/2021/day/17

import re


def read_inputs(filepath):
    with open(filepath) as f:
        return tuple(map(int, re.findall(r"-?\d+", f.read())))


def next_velocity(vx, vy):
    vy -= 1
    if vx == 0:
        return vx, vy
    dx = vx // abs(vx)
    dx *= -1
    vx += dx
    return vx, vy


def simulate(vx, vy, bounds):
    xmin, xmax, ymin, ymax = bounds
    x, y = 0, 0

    highest = 0

    while True:
        x, y = x + vx, y + vy
        vx, vy = next_velocity(vx, vy)

        highest = max(highest, y)

        if x > xmax or y < ymin:
            return False, None

        if xmin <= x <= xmax and ymin <= y <= ymax:
            return True, highest


def solve(bounds):
    ymin = bounds[2]
    best_y = 0
    best_velocity = None
    valids = set()
    min_vy = 1 - ymin

    for vx in range(1, 100):
        for vy in range(-min_vy, min_vy):
            valid, highest = simulate(vx, vy, bounds)
            if valid:
                valids.add((vx, vy))
                if highest > best_y:
                    best_y = highest
                    best_velocity = vx, vy

    return best_y, best_velocity, valids


def main(filepath):
    bounds = read_inputs(filepath)
    best_y, _, valids = solve(bounds)
    print("Part 1:", best_y)
    print("Part 2:", len(valids))
