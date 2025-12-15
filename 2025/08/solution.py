#!/usr/bin/python3

# CODE WRITTEN BY ANTIGRAVITY

import sys
import math

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, i):
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            if self.size[root_i] < self.size[root_j]:
                root_i, root_j = root_j, root_i
            self.parent[root_j] = root_i
            self.size[root_i] += self.size[root_j]
            return True
        return False

def solve():
    points = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            x, y, z = map(int, line.split(','))
            points.append((x, y, z))
        except ValueError:
            continue

    n = len(points)
    if n == 0:
        return

    # K is determined by input size roughly being "large" or "small" based on example
    # Example has 20 lines -> K=10
    # Input has 1000 lines -> K=1000
    # Let's detect based on N.
    if n <= 20: 
        K = 10
    else:
        K = 1000

    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            p1 = points[i]
            p2 = points[j]
            # Squared distance is sufficient for sorting and faster
            dist_sq = (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2
            edges.append((dist_sq, i, j))

    edges.sort()

    dsu = DSU(n)
    num_components = n
    
    last_u, last_v = -1, -1

    for _, u, v in edges:
        if dsu.union(u, v):
            num_components -= 1
            if num_components == 1:
                last_u, last_v = u, v
                break
    
    result = points[last_u][0] * points[last_v][0]
    print(result)

if __name__ == "__main__":
    solve()
