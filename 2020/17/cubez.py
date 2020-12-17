#!/usr/bin/python3

import collections
import functools
import itertools
import operator
import sys


def dumpstate(cubestate):
    all_ys = sorted(functools.reduce(operator.add, [list(slice.keys()) for slice in cubestate.values()]))
    all_xs = sorted(functools.reduce(operator.add,
                                     [list(line.keys()) for line in
                                      functools.reduce(operator.add,
                                                       [list(slice.values()) for slice in cubestate.values()])]))
    #print('x range: (%d, %d)' % (all_xs[0], all_xs[-1]))
    #print('y range: (%d, %d)' % (all_ys[0], all_ys[-1]))
    
    for z in sorted(cubestate.keys()):
        print('z=%d' % z)
        for y in range(all_ys[0], all_ys[-1] + 1):
            for x in range(all_xs[0], all_xs[-1] + 1):
                sys.stdout.write('#' if cubestate[z][y][x] else '.')
            sys.stdout.write('\n')
        print()


def new_cubestate():
    return collections.defaultdict(lambda: collections.defaultdict(lambda: collections.defaultdict(lambda: False)))


def neighbors(xyz):
    ns = []
    (x, y, z) = xyz
    for (dx, dy, dz) in itertools.product([-1, 0, 1], [-1, 0, 1], [-1, 0, 1]):
        if dx == 0 and dy == 0 and dz == 0:
            continue
        ns.append((dx + x, dy + y, dz + z))
    return ns


def run(cubestate):
    active_neighbors = collections.defaultdict(lambda: 0)
    for (z, cubeslice) in cubestate.items():
        for (y, cubeline) in cubeslice.items():
            for (x, state) in cubeline.items():
                if not state:
                    continue
                for (nx, ny, nz) in neighbors((x, y, z)):
                    if z in cubestate and y in cubestate[z] and x in cubestate[z][y] and cubestate[z][y][x]:
                        #print('({0}, {1}, {2}) has active neighbor ({3}, {4}, {5})'.format(nx, ny, nz, x, y, z))
                        active_neighbors[(nx, ny, nz)] += 1

    newstate = new_cubestate()
    for ((x, y, z), nct) in active_neighbors.items():
        state = cubestate[z][y][x]
        if state:
            newstate[z][y][x] = nct in (2, 3)
        else:
            newstate[z][y][x] = nct == 3
        #print('Set (%d, %d, %d) to %d' % (x, y, z, newstate[z][y][x]))
    return newstate


cubestate = new_cubestate()
input_lines = sys.stdin.readlines()
for y in range(len(input_lines)):
    input_line = input_lines[y].replace('\n', '')
    if not input_line:
        continue
    for x in range(len(input_line)):
        cubestate[0][y][x] = input_line[x] == '#'

#print(cubestate)
print('Before any cycles:')
dumpstate(cubestate)
for i in range(6):
    cubestate = run(cubestate)
    print('')
    print('After %d cycles:' % (i+1))
    dumpstate(cubestate)

active_cubes = 0
for slices in cubestate.values():
    for rows in slices.values():
        for cube in rows.values():
            if cube:
                active_cubes += 1
print(active_cubes)
