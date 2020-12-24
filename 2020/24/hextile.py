#!/usr/bin/python3

import collections
import sys


class Direction:
    EAST = (2, 0)
    SOUTHEAST = (1, -1)
    SOUTHWEST = (-1, -1)
    WEST = (-2, 0)
    NORTHWEST = (-1, 1)
    NORTHEAST = (1, 1)
DirectionMap = (('se', Direction.SOUTHEAST),
                ('sw', Direction.SOUTHWEST),
                ('ne', Direction.NORTHEAST),
                ('nw', Direction.NORTHWEST),
                ('e', Direction.EAST),
                ('w', Direction.WEST))


def Flip(pos, flipped):
    if pos in flipped:
        flipped.remove(pos)
    else:
        flipped.add(pos)


def ParseRoute(line):
    pos = [0, 0]
    
    while line:
        direction = None
        for (token, token_dir) in DirectionMap:
            if line[0:len(token)] == token:
                direction = token_dir
                line = line[len(token):]
                break
        if direction is None:
            raise Exception('Invalid direction: %r' % line)
        
        pos[0] += direction[0]
        pos[1] += direction[1]

    return tuple(pos)


def Neighbors(pos):
    return [(pos[0] + direction[1][0], pos[1] + direction[1][1]) for direction in DirectionMap]


def RunRules(flipped):
    new_flipped = set(flipped)

    black_neighbors = collections.defaultdict(set)
    flipped_adjacent = set()
    for pos in flipped:
        for neighbor in Neighbors(pos):
            black_neighbors[neighbor].add(pos)
            if neighbor in flipped:
                black_neighbors[pos].add(neighbor)
            else:
                flipped_adjacent.add(neighbor)

    for pos in flipped:
        if len(black_neighbors[pos]) == 0 or len(black_neighbors[pos]) > 2:
            Flip(pos, new_flipped)
    for pos in flipped_adjacent:
        if len(black_neighbors[pos]) == 2:
            Flip(pos, new_flipped)

    flipped.clear()
    flipped.update(new_flipped)


flipped = set()
for line in sys.stdin.readlines():
    Flip(ParseRoute(line.replace('\n', '')), flipped)
print('Day 0: %d' % len(flipped))

for i in range(100):
    RunRules(flipped)
    print('Day %d: %d' % (i+1, len(flipped)))
