# https://adventofcode.com/2025/day/10

from collections import deque

from z3 import Int, Optimize

Button = tuple[int, ...]
Joltage = tuple[int, ...]
Machine = tuple[str, list[Button], Joltage]


def read_inputs(filepath) -> list[Machine]:
    with open(filepath) as file:
        machines = []
        for line in file.readlines():
            lights, *buttons, joltage = line.strip().split()

            lights = lights[1:-1]
            buttons = list(
                tuple(map(int, button[1:-1].split(","))) for button in buttons
            )
            joltage = tuple(map(int, joltage[1:-1].split(",")))
            machines.append((lights, buttons, joltage))

        return machines


def press(state: str, button: Button) -> str:
    new_state = list(state)
    for i in button:
        new_state[i] = "#" if new_state[i] == "." else "."
    return "".join(new_state)


def min_lights_presses(machine: Machine) -> int:
    seen = set()
    end_state, buttons, _ = machine
    N = len(end_state)

    queue: deque[tuple[str, int]] = deque([("." * N, 0)])  # state, presses

    best = 2**N

    while queue:
        state, presses = queue.popleft()
        if state == end_state:
            best = min(best, presses)
        if state in seen:
            continue
        seen.add(state)

        for button in buttons:
            queue.append((press(state, button), presses + 1))

    return best


def min_joltage_presses(machine: Machine) -> int:
    _, buttons, joltage = machine
    N = len(buttons)

    X = [Int(f"x{i}") for i in range(N)]

    opt = Optimize()

    # Add optimizer constraints
    max_presses = [min(joltage[i] for i in button) for button in buttons]
    for i, x in enumerate(X):
        opt.add(x >= 0)
        opt.add(x <= max_presses[i])

    # Add equations
    # We want to find the minimum number of presses required to reach the end joltage state
    # Ax = J
    # where A is the matrix of button presses impact on any joltage state
    # and J is the target joltage state
    #
    # For the first machine in the test example, we have:
    #
    #     0 0 0 0 1 1    x1    = j1 = 3
    #     0 1 0 0 0 1    x2    = j2 = 5
    #     0 0 1 1 1 0    x3    = j3 = 4
    #     1 1 0 1 0 1    x4    = j4 = 7
    for j, jolt in enumerate(joltage):
        expr = 0
        for i, button in enumerate(buttons):
            if j in button:
                expr += X[i]
        opt.add(expr == jolt)

    opt.minimize(sum(X))  # Magic happens here

    assert opt.check(), "No solution found"
    model = opt.model()
    solution = [model[x].as_long() for x in X]
    return sum(solution)


def solve(machines: list[Machine], minimizer=min_lights_presses):
    return sum(minimizer(machine) for machine in machines)


def main(filepath):
    machines = read_inputs(filepath)
    print("Part 1:", solve(machines))
    print("Part 2:", solve(machines, minimizer=min_joltage_presses))
