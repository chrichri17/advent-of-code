# https://adventofcode.com/2024/day/17
import re


# Relies on the assumption that the program ends with jnz 0
# and has ONLY ONE jnz instruction
class ChronospatialComputer:
    def __init__(self, program: list[int]):
        assert program[-2:] == [3, 0], "program does not end with jnz 0"
        self.program = program

    def run(self, a: int, b: int, c: int):
        def combo_value(operand):
            if 0 <= operand <= 3:
                return operand
            if operand == 4:
                return a
            if operand == 5:
                return b
            if operand == 6:
                return c
            raise ValueError("Invalid combo operand")

        output = None
        pointer = 0

        while pointer < len(self.program):
            cmd, operand = self.program[pointer], self.program[pointer + 1]
            if cmd == 0:  # adv
                a = a >> combo_value(operand)
            elif cmd == 1:  # bxl
                b = b ^ operand
            elif cmd == 2:  # bst
                b = combo_value(operand) % 8
            elif cmd == 3:  # jnz
                if pointer != len(self.program) - 2:
                    raise RuntimeError("program has more than 1 jnz instruction")
            elif cmd == 4:  # bxc
                b = b ^ c
            elif cmd == 5:  # out
                output = combo_value(operand) % 8
            elif cmd == 6:  # bdv
                b = a >> combo_value(operand)
            elif cmd == 7:  # cdv
                c = a >> combo_value(operand)
            else:
                raise ValueError("Invalid command")
            pointer += 2

        return a, output


def read_inputs(filepath):
    pattern = re.compile(r"\d+")
    with open(filepath) as file:
        a, b, c, *program = list(map(int, pattern.findall(file.read())))
        return a, b, c, ChronospatialComputer(program)


def part1(filepath):
    a, b, c, computer = read_inputs(filepath)
    outputs = []

    while a:
        a, output = computer.run(a, b, c)
        if output is not None:
            outputs.append(output)

    return ",".join(map(str, outputs))


# Inputs is 2,4,1,3,7,5,0,3,1,5,4,1,5,5,3,0 and can be translated to
# do
#     b = a % 8
#     b = b ^ 3
#     c = a >> b
#     a = a >> 3
#     b = b ^ 5
#     b = b ^ c
#     print(b % 8)
# while a
#
# We can reverse engineer the program to find the value of A that will output the program itself.
# We need to start from the end value which is 0 (last printed value, i.e B % 8, is 0)
#
# This means that if we want last printed value to be 0,
# then we need to find the value of A that will go through the above program and print B % 8 == 0
# A here must be in range 0-7 because (1) last A must be 0 and (2) in the last iteration, A = A >> 3 returns 0 only if A is in range 0-7
# A simple brute force approach (range 0-7) shows that A = 6.
#
# Then we now know that the iteration before (n-1) would have an A such that A >> 3 == 6 (so that iteration n yield A == 6 AND B % 8 == 0)
# We can now reverse engineer again to find the right value of A within (6 << 3) and (6 << 3) + 7 (these are the possible A for which A >> 3 == 6)
# that validate against the program and print b % 8 == 3
#
# And so on...
def part2(filepath):
    *_, computer = read_inputs(filepath)

    def reverse_engineer(prog, A):
        if not prog:
            return A

        for i in range(8):
            a = (A << 3) + i
            _, out = computer.run(a, 0, 0)
            if out == prog[-1]:
                # backtrack here to avoid getting stuck in a local minima
                # that will not lead to a solution
                # See more in draft.py
                sub = reverse_engineer(prog[:-1], a)
                if sub is not None:
                    return sub

    return reverse_engineer(computer.program, 0)


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
