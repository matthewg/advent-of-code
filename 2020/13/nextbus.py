#!/usr/bin/python3

import sys


def when_bus(b, target_time):
    mod = target_time % b
    if mod > 0:
        mod = b - mod
    return mod


def int_or_none(b):
    try:
        return int(b)
    except ValueError:
        return None


target_time = int(sys.stdin.readline())
busses = [int_or_none(b)
          for b in sys.stdin.readline().replace('\n', '').split(',')]

# Part 1
busses_with_mods = [(b, when_bus(b, target_time)) for b in busses if b]
busses_with_mods.sort(key=lambda b: b[1])
#print(busses_with_mods)
first_bus = busses_with_mods[0]
print('For bus %d, need to wait %d minutes (answer: %d)' % (first_bus[0], first_bus[1], first_bus[0] * first_bus[1]))

# Part 2
# This doesn't actually run in a useful time.
# The real answer involves more maths than I'm up to doing this late in the evening...
# But plugging the numbers into Wolfram Alpha gave the answer.

timesteps = []
for i in range(len(busses)):
    bus = busses[i]
    if bus is None:
        continue
    if i == 0:
        timesteps.append((0, bus))
    else:
        timesteps.append((bus - (i % bus), bus))
timesteps.sort(key=lambda b: -b[1])
print(timesteps)

t = timesteps[0][0]
while True:
    t += timesteps[0][1]
    busses_with_mods = set(ts[0] == (t % ts[1]) for ts in timesteps)
    if False in busses_with_mods:
        continue
    print(t)
    break
