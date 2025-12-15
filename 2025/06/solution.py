#!/usr/bin/python3
import functools
import sys

lines = sys.stdin.read().strip('\n').split('\n')

col_idx = []
prev_col_idx = -10
pos = 0
while True:
    try:
        pos = lines[0].index(' ', pos)
    except ValueError:
        break
    found_non_space = False
    for line in lines:
        if line[pos] != ' ':
            found_non_space = True
            break
    if not found_non_space:
        col_idx.append(pos)
    pos += 1
col_idx.append(len(lines[0]) + 1)

prev_c = 0
grand_total_1 = 0
grand_total_2 = 0
for c in col_idx:
    values = []
    for line in lines:
        values.append(line[prev_c:c])
    prev_c = c
    operation = values.pop().strip()

    num_values = [int(x.strip()) for x in values]
    if operation == '+':
        sum = functools.reduce(lambda x, y: x + y, num_values, 0)
    elif operation == '*':
        sum = functools.reduce(lambda x, y: x * y, num_values, 1)
    grand_total_1 += sum

    num_values_2 = []
    for i in range(len(values[0]) - 1, -1, -1):
        val = ''.join([v[i] for v in values]).strip()
        if val:
            num_values_2.append(int(val))
    if operation == '+':
        sum = functools.reduce(lambda x, y: x + y, num_values_2, 0)
    elif operation == '*':
        sum = functools.reduce(lambda x, y: x * y, num_values_2, 1)
    grand_total_2 += sum

print(grand_total_1)
print(grand_total_2)

