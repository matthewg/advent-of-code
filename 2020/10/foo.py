#!/usr/bin/python3

import collections
import sys
import utils


def foo(line, state):
    state['jolts'].append(int(line))


state = {'jolts': []}
utils.call_for_lines(foo, state)
jolts = sorted(state['jolts'])
jolts.append(jolts[-1] + 3)

jolt_deltas = collections.defaultdict(lambda: 0)
curr_jolts = 0
for jolt in jolts:
    jolt_delta = jolt - curr_jolts
    print('%d -> %d = %d' % (curr_jolts, jolt, jolt_delta))
    jolt_deltas[jolt_delta] += 1
    curr_jolts = jolt

for jolt_delta in jolt_deltas:
    print('%d: %d' % (jolt_delta, jolt_deltas[jolt_delta]))
