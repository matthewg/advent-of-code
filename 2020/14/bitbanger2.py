#!/usr/bin/python3

import collections
import functools
import itertools
import operator
import re
import sys
import utils


def apply_mask(addr, state):
    addrs = []
    print('Applying masks to %d' % addr)
    print('...a: {0:036b}'.format(addr))
    print('...0: {0:036b}'.format(state['mask']['0']))
    print('...1: {0:036b}'.format(state['mask']['1']))
    print('...X: {0:036b}'.format(state['mask']['X']))
    addr |= state['mask']['1']

    x_bits = state['x_bits']
    #print('x_bits: %r' % x_bits)
    for i in range(2**len(x_bits)):
        xmask_0 = 0
        xmask_1 = 0
        for j in range(len(x_bits)):
            x_bit = 1<<x_bits[j]
            if i & (1<<j):
                xmask_1 |= x_bit
            else:
                xmask_0 |= x_bit
        xaddr = addr
        xaddr &= ~xmask_0
        xaddr |= xmask_1
        addrs.append(xaddr)
        #print('...xmask %d' % i)
        #print('.....0: {0:036b}'.format(xmask_0))
        #print('.....1: {0:036b}'.format(xmask_1))
        #print('.....A: {0:036b} == {0}'.format(xaddr))
    return addrs


def do_write(line, state):
    g = re.match(r'^mem.(\d+). = (\d+)$', line)
    if not g:
        raise Exception('Bad input: %r' % line)
    address = int(g.group(1))
    value = int(g.group(2))
    print('Setting %d:' % value)
    for addr in apply_mask(address, state):
        print(addr)
        state['memory'][addr] = value


def do_mask(line, state):
    mask_line = line.split(' = ')[1]
    mask = {'0': 0, '1': 0, 'X': 0}
    x_bits = []
    for bit in range(36):
        mask_char = mask_line[35 - bit]
        mask[mask_char] |= 1<<bit
        if mask_char == 'X':
            x_bits.append(bit)
    print('mask_0: {0} ({0:036b})'.format(mask['0']))
    print('mask_1: {0} ({0:036b})'.format(mask['1']))
    print('mask_X: {0} ({0:036b})'.format(mask['X']))
    state['mask'] = mask
    state['x_bits'] = x_bits
    print('Got mask with %d x_bits' % len(x_bits))


def do_line(line, state):
    if line.startswith('mask'):
        do_mask(line, state)
    else:
        do_write(line, state)


state = {'mask': {}, 'x_bits': [], 'memory': collections.defaultdict(lambda: 0)}
utils.call_for_lines(do_line, state)
for addr in sorted(state['memory'].keys(), key=int):
    print('{0}: {1} ({1:036b})'.format(addr, state['memory'][addr]))
print(functools.reduce(operator.add, state['memory'].values()))
