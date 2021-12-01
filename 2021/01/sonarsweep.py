#!/usr/bin/python3

import utils


state = {
    'prev_depth': None,
    'depth_increase_count': 0,
}


def has_depth_increase(line, state):
    depth = int(line)
    if state['prev_depth'] is not None and depth > state['prev_depth']:
        state['depth_increase_count'] += 1
    state['prev_depth'] = depth


utils.call_for_lines(has_depth_increase, state)
print(state['depth_increase_count'])
