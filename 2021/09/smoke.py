#!/usr/bin/python3

import sys


class Point:
    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.height = height

    def __str__(self):
        return f'({self.x},{self.y}={self.height})'

    def __hash__(self):
        return (self.x, self.y).__hash__()


class Heightmap:
    def __init__(self):
        self.rows = []
        self.width = 0
        self.height = 0

    def add_row(self, heights):
        y = len(self.rows)
        row = []
        self.rows.append(row)
        for x, height in enumerate(heights):
            row.append(Point(x, y, height))
        self.height += 1
        self.width = len(row)

    def adjacent(self, pt):
        adj = []
        if pt.y > 0:
            adj.append(self.point_at(pt.x, pt.y-1))
        if pt.y < (self.height - 1):
            adj.append(self.point_at(pt.x, pt.y+1))
        if pt.x > 0:
            adj.append(self.point_at(pt.x-1, pt.y))
        if pt.x < (self.width - 1):
            adj.append(self.point_at(pt.x+1, pt.y))
        return adj

    def point_at(self, x, y):
        return self.rows[y][x]


def expand_basin(basin_pts, pt, heightmap):
    for adj_pt in heightmap.adjacent(pt):
        if adj_pt.height == 9:
            continue
        if adj_pt in basin_pts:
            continue
        basin_pts.add(adj_pt)
        expand_basin(basin_pts, adj_pt, heightmap)


heightmap = Heightmap()
for line in sys.stdin.readlines():
    line = line.replace('\n', '')
    heights = map(int, line)
    heightmap.add_row(heights)


low_pt_risk = 0
low_pts = []
for y in range(heightmap.height):
    for x in range(heightmap.width):
        pt = heightmap.point_at(x, y)
        adjacents_values = list(map(lambda adj_pt: adj_pt.height, heightmap.adjacent(pt)))
        if pt.height < min(adjacents_values):
            low_pt_risk += pt.height+1
            low_pts.append(pt)
print(low_pt_risk)

basin_sizes = []
for pt in low_pts:
    basin_pts = set()
    basin_pts.add(pt)
    expand_basin(basin_pts, pt, heightmap)
    print(f'Found basin of size {len(basin_pts)} at low point {pt}')
    basin_sizes.append(len(basin_pts))
basin_sizes.sort()
print(f'Product of three largest basins: {basin_sizes[-3] * basin_sizes[-2] * basin_sizes[-1]}')
