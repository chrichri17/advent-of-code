import math
import re
from collections import Counter, defaultdict, deque, namedtuple
from copy import deepcopy
from dataclasses import dataclass
from functools import cache, lru_cache
from heapq import heappop, heappush
from itertools import permutations, product
from hashlib import md5
import random

# import networkx as nx
# from shapely import LinearRing, Polygon

data = open(0)

operators = {
    "AND": lambda a, b: a & b,
    "OR": lambda a, b: a | b,
    "XOR": lambda a, b: a ^ b,
}


# See https://en.wikipedia.org/wiki/Adder_(electronics)#Full_adder
def full_adder(a, b, cin):
    # Formula from
    # https://en.wikipedia.org/wiki/Adder_(electronics)#/media/File:Fulladder.gif
    #
    #
    # A    XOR B     -> VAL0
    # A    AND B     -> VAL1
    # VAL0 AND Cin   -> VAL2
    # VAL0 XOR Cin   -> SUM
    # VAL1 OR  VAL2  -> Cout
    s = a ^ b ^ cin
    cout = (a & b) or ((a ^ b) & cin)
    return s, cout


wires = {}
gates = []

for line in data:
    if line.isspace():
        break
    w, v = line.split(": ")
    wires[w] = int(v)

M = len(wires) // 2

for line in data:
    inputs, out = line.strip().split(" -> ")
    a, op, b = inputs.split()
    if b.startswith("x"):
        a, b = b, a
    gates.append((op, a, b, out))


def is_direct(gate):
    _, a, b, _ = gate
    return a.startswith("x") or b.startswith("x")


def is_not_direct(gate):
    return not is_direct(gate)


def is_output(gate):
    return gate[-1].startswith("z")


def has_input(*vals):
    return lambda gate: gate[1] in vals or gate[2] in vals


def is_gate(kind):
    return lambda gate: gate[0] == kind


incorrects = set()
# Each of these should be An XOR Bn -> VAL0n
# except for the first one which should be x00 XOR y00 -> z00
fa_gate0 = list(filter(is_gate("XOR"), filter(is_direct, gates)))
for gate in fa_gate0:
    _, a, b, out = gate
    is_first = a == "x00" or b == "x00"
    if is_first:
        if out != "z00":
            incorrects.add(out)
        else:
            continue
    else:
        if out == "z00":
            incorrects.add(out)

    if is_output(gate):
        incorrects.add(out)

print(incorrects)

# Each or these should output to zXX
fa_gate3 = list(filter(is_not_direct, filter(is_gate("XOR"), gates)))
for gate in fa_gate3:
    if not is_output(gate):
        incorrects.add(gate[-1])

print(incorrects)

# chack all output gates
# each of these should be VAL0 XOR Cin -> SUM
# except for the last one which should be the alst carry VAL1 OR  VAL2  -> Cout
output_gates = list(filter(is_output, gates))
for gate in output_gates:
    op, a, b, out = gate
    is_last = out == ("z" + str(M).rjust(2, "0"))
    if is_last:
        if op != "OR":
            incorrects.add(out)
    else:
        if op != "XOR":
            incorrects.add(out)

print(incorrects)

# All fa_gate0 should output to a fa_gate3
for gate in fa_gate0:
    out = gate[-1]
    if out == "z00":
        continue
    matches = list(filter(has_input(out), fa_gate3))
    if not matches:
        incorrects.add(out)


# Each of these outputs should be an input of fa_gate4
# except for the first one which should be the Cin1 of gate 1
fa_gate1 = list(filter(is_gate("AND"), filter(is_direct, gates)))

for gate in fa_gate1:
    _, a, b, out = gate
    is_first = a == "x00" or b == "x00"
    if is_first:
        # Skip the first gate as it is a half adder
        # Meaning it's Cout is just x00 AND y00
        # and this will certainly be the Cin of FA 1 ==> out would be in an AND / XOR gate
        continue
    matches = list(filter(has_input(out), gates))
    if not matches:
        incorrects.add(out)
    elif not is_gate("OR")(matches[0]):
        incorrects.add(out)

print(sorted(incorrects))
