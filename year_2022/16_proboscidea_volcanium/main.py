import re
from collections import deque
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class Valve:
    name: str
    rate: int
    neighbors: dict[str, int]
    idx: int = -1


class Valves:
    """
    Collection of valve.
    """

    def __init__(self, valves: dict[str, Valve]) -> None:
        self._valves = valves
        i = 0
        for valve in valves.values():
            if valve.rate:
                valve.idx = i
                i += 1
        self.nb_nonjammed = i + 1

    def __getitem__(self, name: int) -> Valve:
        return self._valves[name]

    def __len__(self):
        return len(self._valves)


def get_valves(filepath) -> Valves:
    """
    Read and parse the inputs: create a graph from the data.
    """
    pattern = "Valve ([A-Z]{2}).*rate=(\d+).*valves? (.*)"
    graph = {}
    rates = {}

    with open(filepath) as file:
        for line in file.readlines():
            x = re.search(pattern, line.strip())
            name, rate, neighbors = x.groups()
            rate = int(rate)

            graph[name] = neighbors.split(", ")
            rates[name] = rate

    valves = {}
    for name, rate in rates.items():
        valves[name] = Valve(name, rate, get_neighbors(graph, rates, name))
    return Valves(valves)


def get_neighbors(
    graph: dict[str, tuple[int, list[str]]], rates: dict[str, int], root: str
) -> dict[str, int]:
    """
    Get all neighbors of the `root` node using a bfs algorithm.
    """
    neighbors = {}
    visited = {root}
    queue = deque([(0, root)])

    while queue:
        dist, node = queue.popleft()
        for neighbor in graph.get(node):
            if neighbor in visited:
                continue
            visited.add(neighbor)
            if rates[neighbor]:
                # only considernon jammeed valves:
                # there is no point in opening a jammed valve
                neighbors[neighbor] = dist + 1
            queue.append((dist + 1, neighbor))

    return neighbors


# LRU cache is used to speed up the dfs
# Since we are using a cache, we need the arguments
# to be hashable. We could use tuples instead of a bitmask to track
# the opened valves.
@lru_cache(maxsize=None)
def max_pressure(valves: Valves, start: str, bitmask: int, timeleft: int = 30) -> int:
    maxvalue = 0

    for neighbor, dist in valves[start].neighbors.items():
        neighbor = valves[neighbor]
        # Open the valve
        bit = 1 << neighbor.idx
        if bit & bitmask:
            # valve already opened
            continue

        pressure = neighbor.rate * (timeleft - dist - 1)
        if pressure <= 0:
            continue
        maxvalue = max(
            maxvalue,
            max_pressure(valves, neighbor.name, bit | bitmask, timeleft - dist - 1)
            + pressure,
        )

    return maxvalue


def max_pressure_2_workers(valves: Valves, start: str) -> int:
    maxvalue = 0
    # (1 << n) returns 1 with n zeros (bin format)
    # (1 << n) - 1 returns n ones
    max_bitmask = (1 << valves.nb_nonjammed) - 1

    # Check every possible combination.
    # Notes that if a valve is already opened at the beginning,
    # it is ignored during the search. We can use that to
    # partition the search space.
    for bitmask in range((max_bitmask + 1) // 2):
        maxvalue = max(
            maxvalue,
            max_pressure(valves, start, bitmask, 26)
            # `max_bitmask - bitmask` is used to flip the digits of `bitmask`.
            # It does the same as `max_bitmask ^ bitmask`
            + max_pressure(valves, start, max_bitmask - bitmask, 26),
        )

    return maxvalue


def main(filepath):
    valves = get_valves(filepath)
    print("Part 1:", max_pressure(valves, "AA", 0, 30))
    # runs in ~0.5s for in.txt
    print("Part 2:", max_pressure_2_workers(valves, "AA"))
