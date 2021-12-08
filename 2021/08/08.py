#!/usr/bin/python3

import collections
import sys

"""
If it's in 7 but not 1, it's a.

6-sements are 0, 6, and 9.
If it has all of the "1", all but 1 of the "4", and all of the "7" then it's 0.
If it has 1 of the "1", all but 1 of the "4", and all but 1 of the "7" then it's 6.
If it has all of the "1", all of the "4", and all of the "7" then it's 9.
Line missing from 0: d
Line missing from 6: c
Line missing from 9: e

5-segments are 2, 3, 5
If it has all of a, d, c, e it's 2.
If it has a, d, and c but not e, it's 3.
If it has a, d, and e but not c, it's 5.
"""

day1_answer = 0
day2_answer = 0

for line in sys.stdin.readlines():
    possible_mappings = {
        'a': set(['A', 'B', 'C', 'D', 'E', 'F', 'G']),
        'b': set(['A', 'B', 'C', 'D', 'E', 'F', 'G']),
        'c': set(['A', 'B', 'C', 'D', 'E', 'F', 'G']),
        'd': set(['A', 'B', 'C', 'D', 'E', 'F', 'G']),
        'e': set(['A', 'B', 'C', 'D', 'E', 'F', 'G']),
        'f': set(['A', 'B', 'C', 'D', 'E', 'F', 'G']),
        'g': set(['A', 'B', 'C', 'D', 'E', 'F', 'G']),
    }
    
    line = line.replace('\n', '')
    inputs_s, outputs_s = line.split(' | ')
    inputs = list(map(lambda s: ''.join(sorted(list(s))), inputs_s.split(' ')))
    outputs = list(map(lambda s: ''.join(sorted(list(s))), outputs_s.split(' ')))
    patterns = inputs + outputs
    patterns_by_length = collections.defaultdict(set)

    pattern_to_digit = {}
    digit_to_pattern = {}
    for pattern in patterns:
        patterns_by_length[len(pattern)].add(pattern)

    one_wires = set(list(patterns_by_length[2])[0])
    seven_wires = set(list(patterns_by_length[3])[0])
    four_wires = set(list(patterns_by_length[4])[0])
    eight_wires = set(list(patterns_by_length[7])[0])
    nine_wires = None

    pattern_to_digit[list(patterns_by_length[2])[0]] = 1
    pattern_to_digit[list(patterns_by_length[3])[0]] = 7
    pattern_to_digit[list(patterns_by_length[4])[0]] = 4
    pattern_to_digit[list(patterns_by_length[7])[0]] = 8

    # 6-segments are 0, 6, and 9.
    for pattern in patterns_by_length[6]:
        wires = set(pattern)
        if wires.intersection(one_wires) == one_wires:
            # It has all of the 1 -- it could be 0 or 9
            if wires.intersection(four_wires) == four_wires:
                pattern_to_digit[pattern] = 9
                nine_wires = wires
            else:
                pattern_to_digit[pattern] = 0
        else:
            pattern_to_digit[pattern] = 6

    # 5-segments are 2, 3, 5
    for pattern in patterns_by_length[5]:
        wires = set(pattern)
        if wires.intersection(one_wires) == one_wires:
            pattern_to_digit[pattern] = 3
        elif wires.intersection(nine_wires) == wires:
            pattern_to_digit[pattern] = 5
        else:
            pattern_to_digit[pattern] = 2

    #print(f'pattern_to_digit: {pattern_to_digit}')
    output_digits = []
    for output in outputs:
        output_digits.append(str(pattern_to_digit[output]))
        if len(output) in (2, 3, 4, 7):
            day1_answer += 1
    output_i = int(''.join(output_digits))
    #print(f'day2: {output} => {output_i}')
    day2_answer += output_i
print(f'Day1 answer: {day1_answer}')
print(f'Day2 answer: {day2_answer}')
