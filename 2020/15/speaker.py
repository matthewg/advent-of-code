#!/usr/bin/python3

import collections
import sys


def speak_number(turn_number, last_number, starting_numbers, spoken_turn):
    if starting_numbers:
        number = starting_numbers.pop(0)
    elif len(spoken_turn[last_number]) == 1:
        number = 0
    else:
        number = spoken_turn[last_number][-1] - spoken_turn[last_number][-2]
    spoken_turn[number].append(turn_number)
    if len(spoken_turn[number]) > 2:
        spoken_turn[number] = spoken_turn[number][-2:]
    return number


starting_numbers = [int(x) for x in sys.stdin.readline().replace('\n', '').split(',')]
spoken_turn = collections.defaultdict(list)
last_number = None
for i in range(30000000):
    if i % 100000 == 0:
        print('Turn %d (%r complete)' % (i, i/30000000))
    last_number = speak_number(i+1, last_number, starting_numbers, spoken_turn)
print(last_number)
