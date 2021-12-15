#!/usr/bin/python3

import heapq
import sys


class Path:
    def __init__(self, node, cost):
        self.node = node
        self.cost = cost

    def __str__(self):
        return f'{self.node}={self.cost}'

    def __lt__(self, other):
        return self.cost < other.cost

    def __gt__(self, other):
        return self.cost > other.cost

    def _eq__(self, other):
        return self.cost == other.cost

    
class Point:
    def __init__(self, x, y, risk):
        self.x = x
        self.y = y
        self.risk = risk

    def __str__(self):
        return f'({self.x},{self.y}={self.risk})'

    def __lt__(self, other):
        if self.risk < other.risk:
            return True
        elif self.risk > other.risk:
            return False
        else:
            return hash(self) < hash(other)

    def __gt__(self, other):
        if self.risk > other.risk:
            return True
        elif self.risk < other.risk:
            return False
        else:
            return hash(self) > hash(other)

    def __eq__(self, other):
        return hash(self) == hash(other)

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


def Dijkstra(heightmap, source, end):
    cheapest_path_to = {source: 0}
    queue = [Path(source, 0)]
    heapq.heapify(queue)
    prev = {}

    while queue:
        u = heapq.heappop(queue)
        node = u.node
        if u.cost > cheapest_path_to[node]:
            continue
        for neighbor in heightmap.adjacent(node):
            cost_to_neighbor = cheapest_path_to[node] + neighbor.risk
            if neighbor not in cheapest_path_to or cost_to_neighbor < cheapest_path_to[neighbor]:
                cheapest_path_to[neighbor] = cost_to_neighbor
                prev[neighbor] = node
                heapq.heappush(queue, Path(neighbor, cost_to_neighbor))

    path = [end]
    current = end
    while current != start:
        current = prev[current]
        path.append(current)
    for node in list(reversed(path)):
        print(node)
    print(cheapest_path_to[end])


heightmap = Heightmap()
for line in sys.stdin.readlines():
    line = line.replace('\n', '')
    heights = map(int, line)
    heightmap.add_row(heights)

start = heightmap.point_at(0, 0)
end = heightmap.point_at(heightmap.width - 1, heightmap.height - 1)
Dijkstra(heightmap, start, end)

"""
The entire cave is actually five times larger in both dimensions than you thought; the area you originally scanned is just one tile in a 5x5 tile area that forms the full map. Your original map tile repeats to the right and downward; each time the tile repeats to the right or downward, all of its risk levels are 1 higher than the tile immediately up or left of it. However, risk levels above 9 wrap back around to 1. So, if your original map had some position with a risk level of 8, then that same position on each of the 25 total tiles would be as follows:

8 9 1 2 3
9 1 2 3 4
1 2 3 4 5
2 3 4 5 6
3 4 5 6 7
Each single digit above corresponds to the example position with a value of 8 on the top-left tile. Because the full map is actually five times larger in both dimensions, that position appears a total of 25 times, once in each duplicated tile, with the values shown above.
"""
heightmap2 = Heightmap()
heightmap2.width = heightmap.width * 5
heightmap2.height = heightmap.height * 5
for y in range(heightmap2.height):
    heightmap2.rows.append([Point(x, y, 0) for x in range(heightmap2.width)])
for x in range(heightmap.width):
    for y in range(heightmap.height):
        point = heightmap.point_at(x, y)
        for tile_x in range(5):
            for tile_y in range(5):
                point2 = heightmap2.point_at(x + heightmap.width*tile_x, y + heightmap.height*tile_y)
                point2.risk = (point.risk + tile_x + tile_y) % 9
                if point2.risk == 0:
                    point2.risk = 9

start = heightmap2.point_at(0, 0)
end = heightmap2.point_at(heightmap2.width - 1, heightmap2.height - 1)
Dijkstra(heightmap2, start, end)
