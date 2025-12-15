#!/usr/bin/python3
import sys

dial = 50
clicks1 = 0
clicks2 = 0
print('The dial starts by pointing at 50.')
for line in sys.stdin:
    line = line.strip('\n')
    movement = int(line[1:])
    prev_dial = dial

    for _ in range(movement):
        if line[0] == 'L':
            dial -= 1
        else:
            dial += 1
        dial %= 100
        
        if dial == 0:
            clicks2 += 1

    dial %= 100
    if dial == 0:
        clicks1 += 1

print(f'Part 1: {clicks1}')
print(f'Part 2: {clicks2}')