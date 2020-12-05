#!/usr/bin/python3

import collections
import sys

# We never hit any trees on the first row, so skip it and initialize with y=1.
sys.stdin.readline()

class Slope:
    def __init__(self, deltaX, deltaY):
        self.x = 0
        self.y = 1
        self.deltaX = deltaX
        self.deltaY = deltaY
        self.trees = 0

SLOPES = []
for (deltaX, deltaY) in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
    SLOPES.append(Slope(deltaX=deltaX, deltaY=deltaY))

while True:
    row = sys.stdin.readline()
    if not row:
        break

    row = row.replace('\n', '')
    for slope in SLOPES:
        # If deltaY is 1, then every row we go down, we go deltaX across and check for trees.
        # Easy. But if deltaY is N, then we're only going acorss and checking for trees
        # every N rows.
        if (slope.y % slope.deltaY) == 0:
            slope.x += slope.deltaX
            char = row[slope.x % len(row)]

            # Out, out, damn bugs
            #if (slope.deltaX == 3 and slope.deltaY == 1):
            #    charIdx = slope.x % len(row)
            #    outRow = ['x' for _ in range(len(row))]
            #    outRow[charIdx] = char
            #    print('|%s|  |%s|' % (row, ''.join(outRow)))

            if char == '#':
                slope.trees += 1
        slope.y += 1

treeProduct = 1
for slope in SLOPES:
    print('For slope (%d, %d), hit %d trees' % (slope.deltaX, slope.deltaY, slope.trees))
    treeProduct *= slope.trees
print('Tree product: %d' % treeProduct)
