import re
from collections import Counter, defaultdict, deque, namedtuple
from copy import deepcopy
from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import permutations, product
import math
from functools import cache, lru_cache

import networkx as nx

# from shapely import LinearRing, Polygon


data = open(0).read()

edges = defaultdict(set)
E = []

for line in data.splitlines():
    a, b = line.split("-")
    E.append((a, b))
    edges[a].add(b)
    edges[b].add(a)

# triplets = set()
# for node in edges:
#     for neighbor in edges[node]:
#         for neighbor2 in edges[neighbor]:
#             if neighbor2 in edges[node]:
#                 triplets.add(tuple(sorted([node, neighbor, neighbor2])))

# total = 0
# for node, n1, n2 in triplets:
#     if node[0] == "t" or n1[0] == "t" or n2[0] == "t":
#         total += 1
# print(total)

nodes = set(edges)

# Q = deque([((a, b), edges[a] & edges[b]) for a in edges for b in edges[a] if a < b])
# connected = set(k for k, _ in Q)

# i = 0
# while Q:
#     conn, inter = Q.popleft()
#     print(conn)

#     if len(inter) == 0:
#         continue

#     if len(inter) == 1:
#         connected.add(tuple(sorted(conn + (inter.pop(),))))
#         continue

#     for n in inter:
#         d = edges[n] & inter
#         if len(d) > 0:
#             Q.append((tuple(sorted(conn + (n,))), d))


Q = deque([({a, b}, edges[a] & edges[b]) for a in edges for b in edges[a] if a < b])
connected = set()
seen = set(connected)

i = 0
while Q:
    conn, inter = Q.popleft()
    print(conn)

    if len(inter) == 0:
        continue
    if tuple(sorted(conn)) in seen:
        continue
    seen.add(tuple(sorted(conn)))

    if len(inter) == 1:
        connected.add(tuple(sorted(conn | inter)))
        Q.append((conn | inter, set()))
        continue

    for n in inter:
        d = edges[n] & inter
        Q.append((conn | {n}, d))


print(",".join(max(connected, key=len)))

# G = nx.Graph()
# G.add_edges_from(E)

# print(",".join(sorted(max(nx.find_cliques(G), key=len))))
