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
#
# Wait, I see what's going on here.
# So if the delta between two positions is a 3, then that adapter *must* be in the
# chain. So the only possible variance is when the adapter is a 1.
# But if it's 3 1 3... well, you need that 1 in there or the two 3's will be too
# far apart.
#
# So it's a run of >1 1's that's relevant here.
# And for whatever reason, none of the provided inputs have runs of more than 4 1's,
# or any 2's.
#
# So by "default", if a 1-adapter can be either present or absent, then it's
# like a bit in a binary number, and the number of possibilities is 2^n where
# n is the number of 1's that are part of a run-of-length-2+. However!
# When you have a run of *4* 1's... you can't have all *4* of them absent
# or the adapters before and after them will be too far apart in voltage!
# And note that 2**4 - 1 = 7... so that's why it's 7**a and not 8**a,
# because the at least one of them has to be left in which eliminates
# one of the possible variations for that run.
