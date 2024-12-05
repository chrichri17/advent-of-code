# https://adventofcode.com/2024/day/05
from collections import defaultdict, deque


class Graph:
    def __init__(self, edges):
        self.before = defaultdict(set)
        self.after = defaultdict(set)
        self.edges = edges

        for a, b in edges:
            self.before[b].add(a)
            self.after[a].add(b)

    def topological_sort(self, nodes: list):
        topo = []
        indegree = {n: len(self.before[n] & set(nodes)) for n in nodes}
        Q = deque([n for n in indegree if indegree[n] == 0])

        while Q:
            n = Q.popleft()
            topo.append(n)
            for m in self.after[n]:
                if m in indegree:
                    indegree[m] -= 1
                    if indegree[m] == 0:
                        Q.append(m)

        return topo


Page = list[int]


def read_inputs(filepath) -> tuple[Graph, list[Page]]:
    with open(filepath) as file:
        e, p = file.read().split("\n\n")
        edges = list(
            map(lambda x: tuple(map(int, x.strip().split("|"))), e.strip().split("\n"))
        )
        pages = list(
            map(
                lambda x: list(map(int, x.strip().split(","))),
                p.strip().split("\n"),
            )
        )
        return Graph(edges), pages


def sum_middle_values(graph: Graph, pages: list[Page]):
    correct, incorrect = 0, 0
    for page in pages:
        sorted_page = graph.topological_sort(page)
        mid = len(page) // 2
        if sorted_page == page:
            correct += page[mid]
        else:
            incorrect += sorted_page[mid]
    return correct, incorrect


def main(filepath):
    graph, pages = read_inputs(filepath)
    p1, p2 = sum_middle_values(graph, pages)
    print("Part 1:", p1)
    print("Part 2:", p2)
