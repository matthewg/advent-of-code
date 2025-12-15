#!/usr/bin/python3
import re
import sys

total1 = 0
total2 = 0
line = sys.stdin.read().strip('\n')
ranges = line.split(',')
for r in ranges:
    pairs = r.split('-')
    lower = int(pairs[0])
    upper = int(pairs[1])
    for i in range(lower, upper + 1):
        if re.match(r'^(.+)(?:\1)$', str(i)):
            total1 += i
        if re.match(r'^(.+)(?:\1)+$', str(i)):
            total2 += i
print(total1)
print(total2)
