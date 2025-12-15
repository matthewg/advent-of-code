#!/usr/bin/python3
import sys

total_joltage1 = 0
total_joltage2 = 0
for line in sys.stdin:
    line = line.strip('\n')
    jolts = [int(x) for x in line]
    max_jolts1 = 0
    max_jolts2 = 0

    for i in range(99, 9, -1):
        first_digit = int(i / 10)
        second_digit = i % 10
        try:
            first_pos = jolts.index(first_digit)
            second_pos = jolts.index(second_digit, first_pos+1)
            max_jolts1 = i
            break
        except ValueError:
            continue
    total_joltage1 += max_jolts1

    pos = 0
    max_jolts2 = 0
    #print(line)
    for d in range(12):
        #print(f'...Working on digit {d}')
        for i in range(9, -1, -1):
            try:
                #print(f'......Checking {i}')
                new_pos = jolts.index(i, pos)
                if len(jolts) - new_pos < 12 - d:
                    #print(f'.........Not enough digits left')
                    continue
                #print(f'.........Found {i} at position {new_pos}')
                break
            except ValueError:
                #print(f'.........Not found')
                continue
        pos = new_pos + 1
        max_jolts2 += i * 10**(12-d-1)
        #print(f'...{max_jolts2}')
    total_joltage2 += max_jolts2

print(total_joltage1)
print(total_joltage2)