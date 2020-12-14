#!/usr/bin/python3

import collections
import functools
import operator
import re
import sys
import utils


def apply_mask(value, state):
    print('Applying masks to %d' % value)
    print('...v: {0:036b}'.format(value))
    print('...0: {0:036b}'.format(state['mask_0']))
    print('...1: {0:036b}'.format(state['mask_1']))
    value &= ~state['mask_0']
    value |= state['mask_1']
    print('...V: {0:036b} == {0}'.format(value))
    return value


def do_write(line, state):
    g = re.match(r'^mem.(\d+). = (\d+)$', line)
    if not g:
        raise Exception('Bad input: %r' % line)
    address = g.group(1)
    value = apply_mask(int(g.group(2)), state)
    print('Setting %s to %d' % (address, value))
    state['memory'][address] = value


def do_mask(line, state):
    mask = line.split(' = ')[1]
    mask_0 = 0
    mask_1 = 0
    for bit in range(36):
        mask_char = mask[35 - bit]
        if mask_char == '0':
            mask_0 |= 1<<bit
        elif mask_char == '1':
            mask_1 |= 1<<bit
    print('mask_0: {0} ({0:036b})'.format(mask_0))
    print('mask_1: {0} ({0:036b})'.format(mask_1))
    state['mask_0'] = mask_0
    state['mask_1'] = mask_1


def do_line(line, state):
    if line.startswith('mask'):
        do_mask(line, state)
    else:
        do_write(line, state)
    

state = {'mask_0': 0, 'mask_1': 0, 'memory': collections.defaultdict(lambda: 0)}
utils.call_for_lines(do_line, state)
for addr in sorted(state['memory'].keys(), key=int):
    print('{0}: {1} ({1:036b})'.format(addr, state['memory'][addr]))
print(functools.reduce(operator.add, state['memory'].values()))
