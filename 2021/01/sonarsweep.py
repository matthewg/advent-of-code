#!/usr/bin/python3

import utils


class Depth1:
    def __init__(self):
        self.depth = None
        self.depth_increase_count = 0

    def new_depth(self, depth):
        if self.depth is not None and depth > self.depth:
            self.depth_increase_count += 1
        self.depth = depth


class Depth3Window:

    def __init__(self):
        self.depth1 = None
        self.depth2 = None
        self.depth3 = None

    def new_depth(self, depth):
        if self.depth1 is None:
            #print('Adding {} to depth1'.format(depth))
            self.depth1 = depth
        elif self.depth2 is None:
            #print('Adding {} to depth2'.format(depth))
            self.depth2 = depth
        elif self.depth3 is None:
            #print('Adding {} to depth3'.format(depth))
            self.depth3 = depth
        else:
            #print('Adding {} to depth3 and discarding depth1'.format(depth))
            self.depth1 = self.depth2
            self.depth2 = self.depth3
            self.depth3 = depth

    def depth(self):
        if self.depth1 is None or self.depth2 is None or self.depth3 is None:
            return None
        return self.depth1 + self.depth2 + self.depth3


state = {
    'depth1': Depth1(),
    'depth3_windows': [Depth3Window(), Depth3Window(), Depth3Window()],
    'depth3_increase_count': 0,
}


def saw_depth(line, state, line_idx):
    depth = int(line)
    #print('Got depth {}'.format(depth))
    state['depth1'].new_depth(depth)

    for (window_idx, prev_window_idx) in ((0, 2), (1, 0), (2, 1)):
        depth3_window = state['depth3_windows'][window_idx]
        depth3_prev = state['depth3_windows'][prev_window_idx]

        depth3_window.new_depth(depth)
        if depth3_window.depth3 is not None:
            window_depth = depth3_window.depth()
            prev_window_depth = depth3_prev.depth()
            #print('Depth {} has window={}, prev={}'.format(depth, window_depth, prev_window_depth))
            if prev_window_depth is not None and window_depth > prev_window_depth:
                state['depth3_increase_count'] += 1            


utils.call_for_lines(saw_depth, state)
print(state['depth1'].depth_increase_count)
print(state['depth3_increase_count'])
