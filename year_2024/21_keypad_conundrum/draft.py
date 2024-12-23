import re
from collections import Counter, defaultdict, deque, namedtuple
from copy import deepcopy
from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import permutations, product
import math
from functools import cache, lru_cache


# import networkx as nx
# from shapely import LinearRing, Polygon

data = open(0).read()

codes = data.splitlines()

num_keypad = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    [None, "0", "A"],
]
num_keypad = tuple(tuple(row) for row in num_keypad)
ns = (3, 2)
num_pos = {num_keypad[r][c]: (r, c) for r in range(4) for c in range(3)}

# nnr, nnc = 4, 3

dir_keypad = [
    [None, "^", "A"],
    ["<", "v", ">"],
]
dir_keypad = tuple(tuple(row) for row in dir_keypad)
ds = (0, 2)
dir_pos = {dir_keypad[r][c]: (r, c) for r in range(2) for c in range(3)}
# dnr, dnc = 2, 3

priority = "v<>^"


def timeit(f):
    def wrapper(*args, **kwargs):
        import time

        start = time.time()
        res = f(*args, **kwargs)
        print(f"{f.__name__} took {time.time() - start:.5f}s")
        return res

    return wrapper


@cache
def go_to(keypad, r, c, val):
    Q = deque([(r, c, "")])
    nr, nc = len(keypad), len(keypad[0])

    all_possibilities = []
    best = math.inf

    while Q:
        cr, cc, path = Q.popleft()
        if keypad[cr][cc] == val:
            if best < len(path):
                break
            best = len(path)
            all_possibilities.append(path + "A")

        for dr, dc, d in [(0, 1, ">"), (0, -1, "<"), (1, 0, "v"), (-1, 0, "^")]:
            sr, sc = cr + dr, cc + dc
            if sr < 0 or sr >= nr or sc < 0 or sc >= nc:
                continue
            if keypad[sr][sc] is None:
                continue
            Q.append((sr, sc, path + d))

    return all_possibilities


# @timeit

CACHE = {}


def solve(code, keypad, pos):
    if (code, keypad) in CACHE:
        return CACHE[(code, keypad)]

    possibilities = {""}
    curr = "A"
    for c in code:
        nf = set()
        for p in go_to(keypad, *pos[curr], c):
            for q in possibilities:
                nf.add(q + p)
        possibilities = nf
        curr = c

    CACHE[(code, keypad)] = possibilities

    return possibilities


total = 0

for code in codes:
    possibilities = solve(code, num_keypad, num_pos)

    for _ in range(5):
        new_possibilities = set()
        for p in possibilities:
            new_possibilities |= solve(p, dir_keypad, dir_pos)
        minlen = len(min(new_possibilities, key=len))
        possibilities = {p for p in new_possibilities if len(p) == minlen}
        # print(len(possibilities)) # exponential growth

    ins = min(possibilities, key=len)
    print(len(ins), "*", int(code[:-1]))
    total += len(ins) * int(code[:-1])
    # break

print(total)
