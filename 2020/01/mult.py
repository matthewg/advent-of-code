#!/usr/bin/python3

import sys

TARGET_SUM = 2020

inputs = [int(line) for line in sys.stdin.readlines()]

found_two = False
found_three = False
for i in range(len(inputs)):
    input_i = inputs[i]
    for j in range(0, i):
        input_j = inputs[j]
        if input_i + input_j == TARGET_SUM:
            print('%d + %d = target; * = %d' % (input_i, input_j, input_i * input_j))
            found_two = True
        for k in range(0, j):
            input_k = inputs[k]
            if input_i + input_j + input_k == TARGET_SUM:
                print('%d + %d + %d = target; * = %d' % (input_i, input_j, input_k, input_i * input_j * input_k))
                found_three = True

if found_two and found_three:
    sys.exit(0)
else:
    sys.stderr.write('No valid inputs found (2=%r, 3=%r)!\n' % (found_two, found_three))
    sys.exit(1)
