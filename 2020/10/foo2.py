#!/usr/bin/python3

import collections
import functools
import sys
import utils


def foo(line, state):
    state['jolts'].append(int(line))


def find_combinations(deltas):
    if len(deltas) == 1:
        return 1

    deltas = deltas[:]
    delta = deltas.pop(0)
    deltas[0] += delta
    if deltas[0] > 3:
        return 1 * find_combinations(deltas)
    else:
        return 2 * find_combinations(deltas)


state = {'jolts': [0]}
utils.call_for_lines(foo, state)
jolts = sorted(state['jolts'])
jolts.append(jolts[-1] + 3)

deltas = []
curr_jolts = 0
for jolt in jolts:
    deltas.append(jolt - curr_jolts)
    curr_jolts = jolt
#combinations = find_combinations(deltas)
print(deltas)

# I don't understand the logic here, but through looking at the two examples, it seems that
# the answer is to look for runs of 1's in the "deltas" list.
#
# Number of runs of 4 1's = a
# Number of runs of 3 1's = b
# Number of runs of 2 1's = c
# Answer = 7**a * 4**b * 2**c
#
# Neither the input nor any of the examples had any "2" in the delta list, only "3", so
# I'm not sure how a 2 would work out...
