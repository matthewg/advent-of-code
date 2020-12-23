#!/usr/bin/python3

import sys


NUM_CUPS = 1_000_000
NUM_MOVES = 10_000_000


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


def Move(first, current, max_4, cup_for_value, moveno):
    #print('-- move %d --' % moveno)
    #print('cups: %s' % FmtCups(first, current))

    picked_up = current.next
    last_picked_up = picked_up.next.next
    current.next = last_picked_up.next
    picked_up_values = (picked_up.value, picked_up.next.value, picked_up.next.next.value)
    #print('pick up: %d, %d, %d' % (picked_up.value, picked_up.next.value, picked_up.next.next.value))

    max_cup = max_4[-1]
    if max_cup.value in picked_up_values:
        max_cup = max_4[-2]
    if max_cup.value in picked_up_values:
        max_cup = max_4[-3]
    if max_cup.value in picked_up_values:
        max_cup = max_4[-4]

    target_value = current.value - 1
    if target_value == 0:
        target_value = max_cup.value
    while target_value in picked_up_values:
        target_value -= 1
        if target_value == 0:
            target_value = max_cup.value
    dest = cup_for_value[target_value]

    #print('dest: %d' % dest.value)
    last_picked_up.next = dest.next
    dest.next = picked_up
    
    #print('')
    return current.next


cups = [Cup(int(c)) for c in sys.stdin.readline().replace('\n', '')]
for i in range(10, NUM_CUPS + 1):
    cups.append(Cup(int(i)))
max_4 = cups[-4:]

current = cups[0]
cup_for_value = {}
for i in range(NUM_CUPS):
    cup_for_value[cups[i].value] = cups[i]
    cups[i].next = cups[(i+1)%len(cups)]

for i in range(NUM_MOVES):
    current = Move(cups[0], current, max_4, cup_for_value, i + 1)
#print('-- final --')
#print('cups: %s' % FmtCups(cups[0], current))

cup = cup_for_value[1]
print('Part 2 answer: %d' % (cup.next.value * cup.next.next.value))
