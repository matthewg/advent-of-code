#!/usr/bin/python3

import utils


class Vector:
    # This is surely part of the Python standard library somewhere,
    # but it'll be faster to implement than find.

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def add(self, vector):
        self.x += vector.x
        self.y += vector.y

    def __str__(self):
        return '({} * {}) => {}'.format(self.x, self.y, self.x*self.y)


def execute_command(command, state, _):
    (direction_s, magnitude_s) = command.split(' ')
    magnitude = int(magnitude_s)
    vector = {
        'forward': Vector(magnitude, 0),  # Day 1 only
        'down': Vector(0, magnitude),  # Y coordinate is *depth*, so 'down' increases it
        'up': Vector(0, -magnitude),
    }[direction_s]

    # Day 1
    state['position1'].add(vector)

    if direction_s == 'forward':
        vector = Vector(magnitude, magnitude*state['aim'])
        state['position2'].add(vector)
        #print('day2: Aim of {} added {}, now at {}'.format(state['aim'], vector, state['position2']))
    elif direction_s == 'down':
        state['aim'] += magnitude
    elif direction_s == 'up':
        state['aim'] -= magnitude


state = {'position1': Vector(), 'position2': Vector(), 'aim': 0}
utils.call_for_lines(execute_command, state)
print('Day 1 rules: {}'.format(state['position1']))
print('Day 2 rules: {}'.format(state['position2']))
