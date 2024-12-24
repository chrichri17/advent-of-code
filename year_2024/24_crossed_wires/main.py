# https://adventofcode.com/2024/day/24

from collections import namedtuple

Gate = namedtuple("Gate", "op a b out")


# Gate filters
def is_input(gate):
    return gate.a.startswith("x") or gate.b.startswith("x")


def is_not_input(gate):
    return not is_input(gate)


def is_output(gate):
    return gate.out.startswith("z")


def has_input(val):
    return lambda gate: gate.a == val or gate.b == val


def is_gate(kind):
    return lambda gate: gate.op == kind


operators = {
    "AND": lambda a, b: a & b,
    "OR": lambda a, b: a | b,
    "XOR": lambda a, b: a ^ b,
}


def read_inputs(filepath):
    with open(filepath) as file:
        wires = {}
        gates = []
        for line in file:
            if line.isspace():
                break
            w, v = line.split(": ")
            wires[w] = int(v)

        for line in file:
            inputs, out = line.strip().split(" -> ")
            a, op, b = inputs.split()
            gates.append(Gate(op, a, b, out))

        return wires, gates


def part1(filepath):
    wires, gates = read_inputs(filepath)
    out_to_gate = {gate.out: gate for gate in gates}

    def get_output(wire):
        if wire in wires:
            return wires[wire]
        op, a, b, _ = out_to_gate[wire]
        wires[wire] = operators[op](get_output(a), get_output(b))
        return wires[wire]

    out_wires = sorted(
        [gate.out for gate in gates if gate.out.startswith("z")], reverse=True
    )
    return int("".join(map(str, map(get_output, out_wires))), 2)


"""
To solve part 2, we reverse engineer the Adder circuit to find the misplaced wires.

A quick look at the inputs reveals it is a set of full adders.
See https://en.wikipedia.org/wiki/Adder_(electronics)#Full_adder


Rules:
- First adder is a half adder (Cin is 0 and Cout = A AND B)
- Each wire output is the sum S of the adder except the last one which is the Cout of the last adder

Here are the logical gates for a full adder:
See https://en.wikipedia.org/wiki/Adder_(electronics)#/media/File:Fulladder.gif

fa_gate0:      A    XOR B     -> VAL0
fa_gate1:      A    AND B     -> VAL1
fa_gate2:      Cin  AND VAL0  -> VAL2
fa_gate3:      VAL0 XOR Cin   -> SUM
fa_gate4:      VAL1 OR  VAL2  -> Cout

Cin is the carry from the previous adder.
Cout is the carry to the next adder.
SUM is the zNN value.


Let's use this logic to find out the misplaced wires.
Solution re-callibrated following https://github.com/piman51277/AdventOfCode/blob/master/solutions/2024/24/index2hand.js
Credits to piman51277
"""


def part2(filepath):
    _, gates = read_inputs(filepath)
    M = len(gates) // 2

    incorrects = set()

    # check fa_gate0
    # Each of the fa_gate0 should be xNN XOR yNN -> VAL0NN
    # except for the first one which should be x00 XOR y00 -> z00
    fa_gates0 = list(filter(is_gate("XOR"), filter(is_input, gates)))
    for gate in fa_gates0:
        is_first = gate.a == "x00" or gate.b == "x00"
        if is_first:
            if gate.out != "z00":
                incorrects.add(gate.out)
            else:
                continue
        else:
            if gate.out == "z00":
                incorrects.add(gate.out)

        if is_output(gate):
            incorrects.add(gate.out)

    # check fa_gate3
    # Each of the gate3 output should be zNN
    fa_gates3 = list(filter(is_not_input, filter(is_gate("XOR"), gates)))
    for gate in fa_gates3:
        if not is_output(gate):
            incorrects.add(gate.out)

    # check output gates
    # Each of the output gates should be VAL0 XOR Cin -> SUM
    # except for the last one which should be the last carry VAL1 OR  VAL2  -> Cout
    output_gates = list(filter(is_output, gates))
    for gate in output_gates:
        is_last = gate.out == (f"z{M:02d}")
        if is_last:
            if gate.op != "OR":
                incorrects.add(gate.out)
        else:
            if gate.op != "XOR":
                incorrects.add(gate.out)

    # check that all fa_gate0 should output to a fa_gate3
    for gate in fa_gates0:
        if gate.out == "z00":
            continue
        matches = list(filter(has_input(gate.out), fa_gates3))
        if not matches:
            incorrects.add(gate.out)

    # check fa_gate1
    # Each of the output should be an input of a fa_gate4
    # except for the first one which should be the Cin1 of gate 1
    fa_gates1 = list(filter(is_gate("AND"), filter(is_input, gates)))
    for gate in fa_gates1:
        is_first = gate.a == "x00" or gate.b == "x00"
        if is_first:
            continue
        matches = list(filter(has_input(gate.out), gates))
        if not matches:
            incorrects.add(gate.out)
        elif gate.out == is_gate("OR")(matches[0]):
            incorrects.add(gate.out)

    if len(incorrects) != 8:
        raise ValueError("Current reverse engineering is incomplete")

    return ",".join(sorted(incorrects))


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
