#!/usr/bin/python3

import sys


class Node:
    def __init__(self, label):
        self.label = label
        self.small = label == label.lower()
        self.adj = set()


def FindPaths(start, end, visited, predecessors, paths, day2, day2_has_revisit):
    #print(f'{".." * len(predecessors)}Finding path from {start.label} to {end.label}...')
    predecessors = list(predecessors)
    predecessors.append(start)
    visited = set(visited)
    visited.add(start)
    if start == end:
        paths.append(predecessors)
        return

    for successor in start.adj:
        this_day2_has_revisit = day2_has_revisit
        if predecessors and predecessors[-1] == successor:
            #print(f'{".." * len(predecessors)}Skipping {successor.label} since we just came from it!')
            continue
        if successor.small and successor in visited:
            #print(f'{".." * len(predecessors)}Skipping {successor.label} since already-visited small!')
            if day2_has_revisit or not day2 or successor.label == 'start' or successor.label == 'end':
                continue
            else:
                this_day2_has_revisit = True
        #print(f'{".." * len(predecessors)}Trying {successor.label}')
        FindPaths(successor, end, visited, predecessors, paths, day2, this_day2_has_revisit)


nodes = {}
for line in sys.stdin.readlines():
    line = line.replace('\n', '')
    (start_s, end_s) = line.split('-')

    start = nodes.get(start_s)
    if not start:
        start = Node(start_s)
        nodes[start_s] = start

    end = nodes.get(end_s)
    if not end:
        end = Node(end_s)
        nodes[end_s] = end

    start.adj.add(end)
    end.adj.add(start)


#for node in nodes.values():
#    print(f'Node {node.label} has adj: {",".join(list(map(lambda a: a.label, node.adj)))}')
paths = []
FindPaths(nodes['start'], nodes['end'], set(), [], paths, True, False)
for path in paths:
    print(','.join(list(map(lambda node: node.label, path))))
print(f'Found {len(paths)} paths.')
