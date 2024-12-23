# https://adventofcode.com/2024/day/23

import networkx as nx


def read_inputs(filepath):
    with open(filepath) as file:
        edges = [l.split("-") for l in file.read().splitlines()]
        return nx.Graph(edges)


def part1(filepath):
    G = read_inputs(filepath)
    triplets = set()
    for node in G.nodes:
        for n1 in G[node]:
            for n2 in G[n1]:
                if n2 in G[node] and (node[0] == "t" or n1[0] == "t" or n2[0] == "t"):
                    triplets.add(tuple(sorted([node, n1, n2])))
    return len(triplets)


def part2(filepath):
    cliques = nx.find_cliques(read_inputs(filepath))
    return ",".join(sorted(max(cliques, key=len)))


def main(filepath):
    print("Part 1:", part1(filepath))
    print("Part 2:", part2(filepath))
