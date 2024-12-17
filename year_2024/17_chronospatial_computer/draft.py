import re
from collections import Counter, defaultdict, deque, namedtuple
from copy import deepcopy
from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import permutations
from shapely import Polygon, LinearRing
import networkx as nx
import math

data = open(0).read().strip()

pattern = re.compile(r"-?\d+")
A, B, C, *program = list(map(int, pattern.findall(data)))

register = dict(A=A, B=B, C=C)

Register = dict[str, int]


outputs = []


def operand_value(operand, t: str):
    if t == "literal":
        return operand
    elif t == "combo":
        if 0 <= operand <= 3:
            return operand
        if operand == 4:
            return register["A"]
        if operand == 5:
            return register["B"]
        if operand == 6:
            return register["C"]
        if operand == 7:
            raise ValueError("Invalid combo operand")
    raise ValueError("Invalid operand")


def combo_value(register, operand):
    if 0 <= operand <= 3:
        return operand
    if operand == 4:
        return register["A"]
    if operand == 5:
        return register["B"]
    if operand == 6:
        return register["C"]
    raise ValueError("Invalid combo operand")


def adv(register: Register, operand: int):
    operand = combo_value(register, operand)
    register["A"] = register["A"] // (2**operand)
    return "", None


def bxl(register: Register, operand: int):
    # xor
    register["B"] = register["B"] ^ operand
    return "", None


def bst(register: Register, operand: int):
    # set bit
    operand = combo_value(register, operand)
    register["B"] = operand % 8
    return "", None


# jump
def jnz(register: Register, operand: int):
    if register["A"] == 0:
        return "", None
    return "", operand


def bxc(register: Register, operand: int):
    register["B"] = register["B"] ^ register["C"]
    return "", None


def out(register: Register, operand: int):
    operand = combo_value(register, operand)
    return str(operand % 8), None


def bdv(register: Register, operand: int):
    operand = combo_value(register, operand)
    register["B"] = register["A"] // (2**operand)
    return "", None


def cdv(register: Register, operand: int):
    operand = combo_value(register, operand)
    register["C"] = register["A"] // (2**operand)
    return "", None


instructions = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]


def execute(register: Register, program: list[int]):
    outputs = []
    i = 0
    while i < len(program):
        op, operand = program[i], program[i + 1]
        assert operand == operand % 8
        # print(op, instructions[op].__name__, operand, end=" ")
        output, jump = instructions[op](register, operand)
        # print(register, (jump, output))
        if output:
            outputs.append(output)
        if jump != None:
            i = jump
        else:
            i += 2

    return outputs


def run(register: Register, program: list[int]):
    out = None
    for p in range(0, len(program), 2):
        op, operand = program[p], program[p + 1]
        assert operand == operand % 8
        output, jump = instructions[op](register, operand)
        if output:
            out = output
    return register["A"], int(out)


# print(",".join(execute(register, program)))


def infunc(a):
    b = a % 8
    b = b ^ 3
    c = a >> b
    a = a >> 3
    b = b ^ 5
    b = b ^ c
    return a, b % 8


def testfunc(a):
    a = a >> 1
    b = a % 8
    return a, b


# a = 729
# while a:
#     a, b = testfunc(a)
#     print(b, end=",")

# a = 63687530
# while a:
#     a, b = infunc(a)
#     print(b, end=",")

# 7 -> 0
curr = 0
idx = len(program) - 1

print(program)
# print(execute(dict(A=6, B=0, C=0), program))
print(infunc(1610370))
print(run(dict(A=1610370, B=0, C=0), program))
# print(infunc(201296))
# print(infunc(25162))
# print(infunc(3145))
# print(infunc(393))
# print(infunc(49))
# print(infunc(6))


def backtrack(prog, A):
    if prog == []:
        print("Ending", A)
        return A

    for i in range(8):
        a = (A << 3) + i
        print(f"Searching... {A = } {a = } target = {prog[-1]}")
        a, out = run(dict(A=a, B=0, C=0), program)
        # a, out = infunc(a)
        if out == prog[-1]:
            print("   Found but backtracking", (A << 3) + i, out)
            sub = backtrack(prog[:-1], (A << 3) + i)
            if sub is None:
                continue
            return sub


print(backtrack(program, 0))

# br = 0
# while idx >= 0:
#     for i in range(8):
#         print("in loop", i, (curr << 3) + i, end=" ")
#         a, out = infunc((curr << 3) + i)
#         print(a, out)
#         if out == program[idx]:
#             print("breaking", i)
#             curr = (curr << 3) + i
#             idx -= 1
#             break

#     print(a, curr, i, idx)
#     # Local minima ==> stucked. Due to the fact that there might be multiple value fullfilling the condition but we break too soon
#     if idx == 8:
#         if br == 2:
#             break
#         else:
#             br += 1
# break
