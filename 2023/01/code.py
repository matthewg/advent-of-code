#!/usr/bin/python3
import utils

import functools


def find_number(s, state, line_idx):
    orig_s = s
    #numbers = [int(c) for c in s if c.isdigit()]
    #state['numbers'].append(numbers[0] * 10 + numbers[-1])

    mop = [('one', '1'),
           ('two', '2'),
           ('three', '3'),
           ('four', '4'),
           ('five', '5'),
           ('six', '6'),
           ('seven', '7'),
           ('eight', '8'),
           ('nine', '9'),
           ]
    idx = 0
    while idx < len(s):
        for word, number in mop:
            if s[idx:idx+len(word)] == word:
                s = s[:idx] + number + s[idx+1:]
                break
        idx += 1
    numbers = [int(c) for c in s if c.isdigit()]
    number = numbers[0] * 10 + numbers[-1]
    print(f'{orig_s} => {s} => {number}')
    state['numbers2'].append(number)


state = {'numbers': [], 'numbers2': []}
utils.call_for_lines(find_number, state)

#sum = functools.reduce(lambda a, b: a + b, state['numbers'], 0)
#print(state['numbers'])
#print(sum)

sum = functools.reduce(lambda a, b: a + b, state['numbers2'], 0)
print(sum)
