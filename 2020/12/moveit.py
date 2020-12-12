#!/usr/bin/python3

import utils


NORTH = 'N'
SOUTH = 'S'
EAST = 'E'
WEST = 'W'
LEFT = 'L'
RIGHT = 'R'
FORWARD = 'F'


def moveit(line, state):
    move = line[0]
    magnitude = int(line[1:])

    rotate = 0
    vector = (0, 0)
    if move == RIGHT:
        rotate = magnitude
    elif move == LEFT:
        rotate = -magnitude
    elif move == NORTH:
        vector = (0, 1)
    elif move == SOUTH:
        vector = (0, -1)
    elif move == EAST:
        vector = (1, 0)
    elif move == WEST:
        vector = (-1, 0)
    elif move == FORWARD:
        vector = state['direction']
    else:
        raise Exception('Invalid input: %r' % line)

    state['x'] += vector[0]*magnitude
    state['y'] += vector[1]*magnitude
    if rotate:
        direction = state['direction']
        for _ in range(int((rotate % 360) / 90)):
            if direction == (1, 0):
                direction = (0, -1)
            elif direction == (0, -1):
                direction = (-1, 0)
            elif direction == (-1, 0):
                direction = (0, 1)
            elif direction == (0, 1):
                direction = (1, 0)
            else:
                raise Exception('Invalid direction: %r' % direction)
        state['direction'] = direction

state = {'direction': (1, 0), 'x': 0, 'y': 0}
utils.call_for_lines(moveit, state)
print('At (%d, %d), %d from origin' % (state['x'], state['y'], abs(state['x']) + abs(state['y'])))
