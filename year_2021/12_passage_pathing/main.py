# https://adventofcode.com/2021/day/12

from collections import defaultdict, deque


def read_inputs(filepath):
    with open(filepath) as file:
        edges = defaultdict(list)
        for line in file.readlines():
            a, b = line.strip().split("-")
            edges[a].append(b)
            edges[b].append(a)
        return edges


def part1(filepath):
    edges = read_inputs(filepath)

    Q = deque([("start", set())])
    nb_paths = 0

    while Q:
        node, visited = Q.popleft()
        if node == "end":
            nb_paths += 1
            continue

        for neighbor in edges[node]:
            if neighbor in visited or neighbor == "start":
                continue
            new_visited = (
                visited | {neighbor} if neighbor.lower() == neighbor else set(visited)
            )
            Q.append((neighbor, new_visited))

    return nb_paths


def part2(filepath):
    edges = read_inputs(filepath)

    Q = deque([("start", set(), False)])
    nb_paths = 0

    while Q:
        node, visited, twice = Q.popleft()
        if node == "end":
            nb_paths += 1
            continue

        for neighbor in edges[node]:
            if neighbor == "start":
                # skip start node
                continue
            if neighbor in visited and twice:
                # skip if at least one small node is visited twice
                continue
            new_visited = (
                visited | {neighbor} if neighbor.lower() == neighbor else set(visited)
            )
            if neighbor in visited and not twice:
                Q.append((neighbor, new_visited, True))
            else:
                Q.append((neighbor, new_visited, twice))

    return nb_paths


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
