#!/usr/bin/python3

import collections
import re
import utils


def process_line(line, state, _):
    match = re.match(r'(\d+),(\d+) -> (\d+),(\d+)', line)
    p1 = (int(match.group(1)), int(match.group(2)))
    p2 = (int(match.group(3)), int(match.group(4)))

    for p in (p1, p2):
        if p[0] < state['min_x']:
            state['min_x'] = p[0]
        if p[0] > state['max_x']:
            state['max_x'] = p[0]
        if p[1] < state['min_y']:
            state['min_y'] = p[1]
        if p[1] > state['max_y']:
            state['max_y'] = p[1]

    p_delta = [0,0]
    if p1[0] > p2[0]:
        p_delta[0] = -1
    elif p1[0] < p2[0]:
        p_delta[0] = 1

    if p1[1] > p2[1]:
        p_delta[1] = -1
    elif p1[1] < p2[1]:
        p_delta[1] = 1    

    p = list(p1)

    print('Processing {}, p_delta={}'.format(line, p_delta))
    while True:
        # Uncomment for day 1:
        # if p_delta[0] ^ p_delta[1]:
        state['field'][p[0]][p[1]] += 1
        #print('p={}'.format(p))

        if p[0] == p2[0] and p[1] == p2[1]:
            return

        p[0] += p_delta[0]
        p[1] += p_delta[1]


state = {
    'field': collections.defaultdict(lambda: collections.defaultdict(lambda: 0)),
    'min_x': 0,
    'min_y': 0,
    'max_x': 0,
    'max_y': 0,
}
utils.call_for_lines(process_line, state)

twopoints = 0
for y in range(state['min_y'], state['max_y'] + 1):
    row = state['field'][y]
    cells = []
    for x in range(state['min_x'], state['max_x'] + 1):
        if row[x] > 0:
            if row[x] >= 2:
                twopoints += 1
            cells.append(str(row[x]))
        else:
            cells.append('.')
    print(''.join(cells))

print(twopoints)
