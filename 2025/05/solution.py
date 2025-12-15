#!/usr/bin/python3
import sys

fresh_ranges = []

for line in sys.stdin:
    line = line.strip('\n')
    if line == '':
        break
    r = line.split('-')
    lower = int(r[0])
    upper = int(r[1])
    fresh_ranges.append((lower, upper))

fresh_ranges.sort()
merged = []
for start, end in fresh_ranges:
    if not merged or start > merged[-1][1]:
        merged.append((start, end))
    else:
        merged[-1] = (merged[-1][0], max(merged[-1][1], end))
fresh_ranges = merged

fresh_count = 0
for line in sys.stdin:
    line = line.strip('\n')
    i = int(line)
    for r in fresh_ranges:
        if r[0] > i:
            break
        if i <= r[1]:
            fresh_count += 1
            break
print(fresh_count)

fresh_count = 0
for r in fresh_ranges:
    fresh_count += r[1] - r[0] + 1 
print(fresh_count)
