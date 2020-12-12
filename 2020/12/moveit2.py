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
    wp_vector = (0, 0)
    vector = (0, 0)
    if move == RIGHT:
        rotate = magnitude
    elif move == LEFT:
        rotate = -magnitude
    elif move == NORTH:
        wp_vector = (0, 1)
    elif move == SOUTH:
        wp_vector = (0, -1)
    elif move == EAST:
        wp_vector = (1, 0)
    elif move == WEST:
        wp_vector = (-1, 0)
    elif move == FORWARD:
        vector = (state['wx'], state['wy'])
    else:
        raise Exception('Invalid input: %r' % line)

    state['x'] += vector[0]*magnitude
    state['y'] += vector[1]*magnitude
    state['wx'] += wp_vector[0]*magnitude
    state['wy'] += wp_vector[1]*magnitude
    if rotate:
        normalized_rotate = rotate % 360
        clockwise_rotations = int(normalized_rotate / 90)
        #print('Rotating %r aka %d (%d turns), starting at (%d, %d' % (line, normalized_rotate, clockwise_rotations, wx, wy))
        for _ in range(clockwise_rotations):
            wx = state['wx']
            wy = state['wy']
            state['wx'] = wy
            state['wy'] = -wx
    print('State after %r: %r' % (line, state))

state = {'x': 0, 'y': 0, 'wx': 10, 'wy': 1}
utils.call_for_lines(moveit, state)
print('At (%d, %d), %d from origin' % (state['x'], state['y'], abs(state['x']) + abs(state['y'])))


"""
.....|.....
.....|.....
.....|.o...
.....|.....
.....|.....
=====*=====
.....|.....
.....|.....
.....|.....
.....|.....
.....|.....


(2,3)
(3,-2)
(-2,-3)
(-3,2)
"""

"""
.......|.......
.......|.......
.......|.......
.......|.......
.......|.......
.......|.......
.......|.......
=======*=======
.......|.......
.......|......*
.......|.......
.......|.......
.......|.......
.......|.......
.......|.......


(7,-2)
(-2,-7)
(-7,2)
(2,7)
"""
