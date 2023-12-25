# https://adventofcode.com/2023/day/25

from collections import defaultdict

import networkx as nx


def read_inputs(filepath) -> nx.DiGraph:
    edges = defaultdict(set)
    graph = nx.DiGraph()

    with open(filepath) as file:
        for line in file.readlines():
            u, neighbors = line.split(":")
            for v in neighbors.split():
                edges[u].add(v)
                edges[v].add(u)

        for u, neighbors in edges.items():
            for v in neighbors:
                graph.add_edge(u, v, capacity=1.0)
                graph.add_edge(v, u, capacity=1.0)

    return graph


def part1(filepath):
    graph = read_inputs(filepath)
    nodes = list(graph.nodes)
    src = nodes[0]

    for target in nodes[1:]:
        cut_value, partition = nx.minimum_cut(graph, src, target)
        if cut_value == 3:
            reachable, non_reachable = partition
            return len(reachable) * len(non_reachable)


def part2(filepath):
    return "🎉🎉🎉 Year 2023 done 🎉🎉🎉"


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
