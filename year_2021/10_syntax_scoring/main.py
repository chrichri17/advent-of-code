# https://adventofcode.com/2021/day/10
import re
from collections import defaultdict, deque, Counter
from math import prod, lcm, gcd
import heapq


def read_inputs(filepath):
    with open(filepath) as file:
        for line in file.readlines():
            yield line.strip()


opened_chunks = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

closed_chunks = {v: k for k, v in opened_chunks.items()}


def validate_syntax(line: str) -> int:
    stack = []
    for i, chunk in enumerate(line):
        if chunk in opened_chunks:
            stack.append(chunk)
        else:
            if not stack or stack[-1] != closed_chunks[chunk]:
                return [], i
            stack.pop()
    return stack, -1


def part1(filepath):
    syntax_score = 0
    points = {")": 3, "]": 57, "}": 1197, ">": 25137}
    for line in read_inputs(filepath):
        _, pos = validate_syntax(line)
        if pos != -1:
            syntax_score += points[line[pos]]
    return syntax_score


def part2(filepath):
    scores = []
    points = {")": 1, "]": 2, "}": 3, ">": 4}
    for line in read_inputs(filepath):
        stack, pos = validate_syntax(line)
        if pos != -1:
            continue
        score = 0
        for c in stack[::-1]:
            score = score * 5 + points[opened_chunks[c]]
        scores.append(score)
    scores.sort()
    return scores[len(scores) // 2]


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
