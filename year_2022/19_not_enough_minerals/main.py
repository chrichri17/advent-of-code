import re
from math import ceil


def read_inputs(filepath):
    blueprints = []

    with open(filepath) as file:
        for i, line in enumerate(file.readlines(), 1):
            rules = []
            maxspend = [0, 0, 0]
            for section in line.split(": ")[1].strip().split(". "):
                rule = []
                for x, y in re.findall(r"(\d+) (\w+)", section):
                    x = int(x)
                    y = ["ore", "clay", "obsidian"].index(y)
                    maxspend[y] = max(maxspend[y], x)
                    rule.append((x, y))
                rules.append(rule)
            blueprints.append((rules, maxspend))
    return blueprints




def dfs(blueprint, maxspend, cache, time, bots, amount):
    if time == 0:
        return amount[3]
    key = tuple((time, *bots, *amount))
    if key in cache:
        return cache[key]

    # Five options: Build robot (4 possibilities) or do nothing

    maxval = amount[3] + bots[3] * time

    for bot_type, rule in enumerate(blueprint):
        if bot_type != 3 and bots[bot_type] >= maxspend[bot_type]:
            # There is no point in building more of this bot
            # Geode bot (type == 3) is special since we do need to build them infinitely (target minerals)
            continue

        # How much should we wait to build this bot?
        wait = 0
        for r_amount, r_type in rule:
            if bots[r_type] == 0:
                break
            wait = max(wait, ceil((r_amount - amount[r_type]) / bots[r_type]))
        else:
            # We can build this bot
            remaining_time = time - wait - 1  # -1 for building the bot
            if remaining_time < 0:
                continue
            new_bots = bots[:]
            new_amount = [x + y * (wait + 1) for x, y in zip(amount, bots)]
            # Spend minerals to build the bot
            for r_amount, r_type in rule:
                new_amount[r_type] -= r_amount
            new_bots[bot_type] += 1

            # Optimisation
            for i in range(3):
                # 20:45
                new_amount[i] = min(new_amount[i], maxspend[i] * remaining_time)

            maxval = max(
                maxval,
                dfs(blueprint, maxspend, cache, remaining_time, new_bots, new_amount),
            )

    cache[key] = maxval
    return maxval


def part1(filepath):
    blueprints = read_inputs(filepath)
    print(blueprints)
    total = 0
    for no, (blueprint, maxspend) in enumerate(blueprints, 1):
        cache = {}
        total += dfs(blueprint, maxspend, cache, 24, [1, 0, 0, 0], [0, 0, 0, 0]) * no
    return total


def main(filepath):
    print("Part 1:", part1(filepath))
    print(
        "Part 2:",
    )
