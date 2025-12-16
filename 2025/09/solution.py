#!/usr/bin/python3
import sys

points = []

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    x, y = map(int, line.split(','))
    points.append((x, y))

max_d = 0
for p1 in points:
    for p2 in points:
        d = (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)
        max_d = max(max_d, d)
print(max_d)
