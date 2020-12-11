#!/usr/bin/python3

import collections
import functools
import sys
import utils


FLOOR = '.'
EMPTY = 'L'
OCCUPIED = '#'


def make_seatmap(state):
    return [[FLOOR for _ in range(state['height'])]
            for _ in range(state['width'])]


def neighbors(state, x, y):
    ns = []
    for (dx, dy) in ((-1, -1),
                     (-1, 0),
                     (-1, +1),
                     (0, -1),
                     (0, 1),
                     (1, -1),
                     (1, 0),
                     (1, 1)):
        nx = x
        ny = y
        while True:
            nx += dx
            ny += dy
            if nx < 0 or ny < 0 or nx >= state['width'] or ny >= state['height']:
                # Fell off the end without finding a seat.
                break
            if state['seats'][nx][ny] != FLOOR:
                ns.append((nx, ny))
                break
    return ns


def run(state):
    seats = state['seats']
    new_seats = make_seatmap(state)
    for x in range(state['width']):
        for y in range(state['height']):
            ns = [seats[nx][ny] for (nx, ny) in neighbors(state, x, y)]
            if seats[x][y] == EMPTY and OCCUPIED not in ns:
                new_seats[x][y] = OCCUPIED
            elif seats[x][y] == OCCUPIED and len([s for s in ns if s == OCCUPIED]) >= 5:
                new_seats[x][y] = EMPTY
            else:
                new_seats[x][y] = seats[x][y]
    state['seats'] = new_seats


def print_seats(state):
    for y in range(state['height']):
        for x in range(state['width']):
            sys.stdout.write(state['seats'][x][y])
        print('')


lines = [line.replace('\n', '') for line in sys.stdin.readlines()]
state = {'width': len(lines[0]), 'height': len(lines), 'seats': None}
state['seats'] = make_seatmap(state)
for y in range(len(lines)):
    for x in range(len(lines[0])):
        state['seats'][x][y] = lines[y][x]


while True:
    #print('Step %d:' % i)
    #print_seats(state)
    #print('')

    old_seats = state['seats']
    run(state)
    new_seats = state['seats']

    if old_seats == new_seats:
        break

occupied_count = functools.reduce(lambda a, b: a + int(b == OCCUPIED), functools.reduce(lambda a, b: a + b, state['seats'], []), 0)
print(occupied_count)
