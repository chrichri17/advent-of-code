# https://adventofcode.com/2024/day/22

from collections import defaultdict


def read_inputs(filepath):
    with open(filepath) as file:
        for line in file.readlines():
            yield int(line.strip())


def mix(secret, x):
    return secret ^ x


def prune(secret):
    return secret % 16777216


def simulate(secret, times=2000):
    prices = [secret]
    for _ in range(times):
        secret = prune(mix(secret, secret * 64))
        secret = prune(mix(secret, secret // 32))
        secret = prune(mix(secret, secret * 2048))
        prices.append(secret)
    return prices


def part1(inputs):
    return sum(prices[-1] for prices in inputs)


def part2(inputs):
    buys = defaultdict(int)
    for prices in inputs:
        prices = [price % 10 for price in prices]
        changes = [b - a for a, b in zip(prices, prices[1:])]

        first_occurences = {}
        for i in range(4, len(changes)):
            pattern = tuple(changes[i - 4 : i])
            if pattern not in first_occurences:
                first_occurences[pattern] = prices[i]

        for pattern, value in first_occurences.items():
            buys[pattern] += value

    return max(buys.values())


def main(filepath):
    inputs = [simulate(secret) for secret in read_inputs(filepath)]
    print("Part 1:", part1(inputs))
    print("Part 2:", part2(inputs))
