# https://adventofcode.com/2023/day/20

import math
from collections import Counter, deque
from dataclasses import dataclass, field
from enum import Enum


class State(Enum):
    ON = "on"
    OFF = "off"


class Pulse(Enum):
    LOW = "low"
    HIGH = "high"

    def __str__(self) -> str:
        return str(self._value_)


class ModuleKind(Enum):
    FLIP_FLOP = "%"
    CONJUNCTION = "&"
    BROADCASTER = "broadcaster"


@dataclass
class Module:
    name: str
    kind: ModuleKind
    destinations: tuple[str]
    state: State = State.OFF
    memory: dict[str, Pulse] = field(default_factory=dict)

    def flips_state(self) -> Pulse:
        if self.state == State.OFF:
            self.state = State.ON
            return Pulse.HIGH
        else:
            self.state = State.OFF
            return Pulse.LOW


DEBUG = False


def debug(*args):
    if DEBUG:
        print(*args)


def read_inputs(filepath):
    modules: dict[str, Module] = {}
    brodcaster: Module = Module("broadcaster", ModuleKind.BROADCASTER, [])

    with open(filepath) as file:
        for line in file.readlines():
            mod, _, destinations = line.strip().partition(" -> ")
            destinations = tuple(destinations.split(", "))

            if mod == "broadcaster":
                brodcaster.destinations = destinations
            else:
                kind = ModuleKind(mod[0])
                name = mod[1:]
                modules[name] = Module(name, kind, destinations)

        for module in modules.values():
            for name in module.destinations:
                if name not in modules:
                    continue
                destination = modules[name]
                if destination.kind == ModuleKind.CONJUNCTION:
                    destination.memory[module.name] = Pulse.LOW

    return brodcaster, modules


def part1(filepath):
    broadcaster, modules = read_inputs(filepath)
    N = 1_000

    counter = Counter(lo=N, hi=0)
    for _ in range(N):
        debug(f"button -{Pulse.LOW}-> broadcaster")
        queue = deque(
            [("broadcaster", Pulse.LOW, dest) for dest in broadcaster.destinations]
        )

        while queue:
            src, pulse, dest = queue.popleft()
            debug(f"{src} -{pulse}-> {dest}")

            counter["lo"] += int(pulse == Pulse.LOW)
            counter["hi"] += int(pulse == Pulse.HIGH)

            if dest not in modules:
                continue

            module = modules[dest]

            if module.kind == ModuleKind.FLIP_FLOP:
                if pulse == Pulse.LOW:
                    new_pulse = module.flips_state()
                    for dest in module.destinations:
                        queue.append((module.name, new_pulse, dest))
            elif module.kind == ModuleKind.CONJUNCTION:
                module.memory[src] = pulse
                new_pulse = (
                    Pulse.LOW
                    if all(p == Pulse.HIGH for p in module.memory.values())
                    else Pulse.HIGH
                )
                for dest in module.destinations:
                    queue.append((module.name, new_pulse, dest))

        debug()

    return counter["lo"] * counter["hi"]


def part2(filepath):
    broadcaster, modules = read_inputs(filepath)

    rx_src = next(
        name for name, module in modules.items() if "rx" in module.destinations
    )
    cycles = {
        name: 0 for name, module in modules.items() if rx_src in module.destinations
    }

    btn_presses = 0

    while True:
        btn_presses += 1
        queue = deque(
            [("broadcaster", Pulse.LOW, dest) for dest in broadcaster.destinations]
        )

        while queue:
            src, pulse, dest = queue.popleft()

            if dest not in modules:
                continue

            module = modules[dest]

            # This means that we are sending a high pulse to the conjunction module that will send pulses to rx
            if module.name == rx_src and pulse == Pulse.HIGH:
                if cycles[src] == 0:
                    cycles[src] = btn_presses

                # Check if the cunjunction will send a low pulse
                if all(cycles.values()):
                    return math.lcm(*cycles.values())

            ### Same as before
            if module.kind == ModuleKind.FLIP_FLOP:
                if pulse == Pulse.LOW:
                    new_pulse = module.flips_state()
                    for dest in module.destinations:
                        queue.append((module.name, new_pulse, dest))
            elif module.kind == ModuleKind.CONJUNCTION:
                module.memory[src] = pulse
                new_pulse = (
                    Pulse.LOW
                    if all(p == Pulse.HIGH for p in module.memory.values())
                    else Pulse.HIGH
                )
                for dest in module.destinations:
                    queue.append((module.name, new_pulse, dest))


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
