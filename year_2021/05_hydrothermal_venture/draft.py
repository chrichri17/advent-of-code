import re

lines = []
mr, mc = 0, 0
Mr, Mc = 0, 0

for line in open(0).read().splitlines():
    # pattern x1,y1 -> x2,y2
    x1, y1, x2, y2 = map(int, re.findall(r"(\d+)", line))
    # print((x1, y1), (x2, y2))
    lines.append((x1, y1, x2, y2))
    mr = min(mr, x1, x2)
    Mr = max(Mr, x1, x2)
    mc = min(mc, y1, y2)
    Mc = max(Mc, y1, y2)

points = {}
for line in lines:
    x1, y1, x2, y2 = line
    # horizontal line
    if x1 == x2:
        m, M = min(y1, y2), max(y1, y2)
        for y in range(m, M + 1):
            points[(x1, y)] = points.get((x1, y), 0) + 1
    # vertical line
    if y1 == y2:
        m, M = min(x1, x2), max(x1, x2)
        for x in range(m, M + 1):
            points[(x, y1)] = points.get((x, y1), 0) + 1
    # diagonal 1: x - y = cte
    if x1 - y1 == x2 - y2:
        # print("diagonal x - y = cte", x1, y1, x2, y2)
        x, y = x1, y1
        if x2 < x1:
            x, y = x2, y2
        diff = abs(x2 - x1)
        for i in range(diff + 1):
            # print(x + i, y + i)
            points[(x + i, y + i)] = points.get((x + i, y + i), 0) + 1

    # diagonal 2: x + y = cte
    if x1 + y1 == x2 + y2:
        # print("diagonal x + y = cte", x1, y1, x2, y2)
        x, y = x1, y1
        if x2 < x1:
            x, y = x2, y2
        diff = abs(x2 - x1)
        for i in range(diff + 1):
            # print(x + i, y - i)
            points[(x + i, y - i)] = points.get((x + i, y - i), 0) + 1
    # break

# print(points)
# for y in range(Mc + 1):
#     for x in range(Mr + 1):
#         print(points.get((x, y), "."), end=" ")
#     print()
print(sum(v > 1 for v in points.values()))
