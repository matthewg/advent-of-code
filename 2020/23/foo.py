#!/usr/bin/python3

import sys


NUM_CUPS = 9
NUM_MOVES = 100


class Cup:
    def __init__(self, value):
        self.next = None
        self.value = value


def FmtCups(first, current):
    cup_strs = []
    cup = first
    for _ in range(NUM_CUPS):
        if cup == current:
            cup_strs.append('(%d)' % cup.value)
        else:
            cup_strs.append(' %d ' % cup.value)
        cup = cup.next
    return ''.join(cup_strs)


def Move(first, current, moveno):
    print('-- move %d --' % moveno)
    print('cups: %s' % FmtCups(first, current))

    picked_up = current.next
    last_picked_up = picked_up.next.next
    current.next = last_picked_up.next
    print('pick up: %d, %d, %d' % (picked_up.value, picked_up.next.value, picked_up.next.next.value))

    target_value = current.value - 1
    max_cup = current
    while target_value >= 0:
        dest = current
        for _ in range(NUM_CUPS - 3):
            if dest.value == target_value:
                break
            if dest.value > max_cup.value:
                max_cup = dest
            dest = dest.next
        if dest.value == target_value:
            break
        target_value -= 1
    if target_value == -1:
        dest = max_cup

    print('dest: %d' % dest.value)
    last_picked_up.next = dest.next
    dest.next = picked_up
    
    print('')
    return current.next


cups = [Cup(int(c)) for c in sys.stdin.readline().replace('\n', '')]
current = cups[0]
for i in range(NUM_CUPS):
    cups[i].next = cups[(i+1)%len(cups)]

for i in range(NUM_MOVES):
    current = Move(cups[0], current, i + 1)
print('-- final --')
print('cups: %s' % FmtCups(cups[0], current))
