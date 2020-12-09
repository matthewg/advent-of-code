#!/usr/bin/python3

import sys
import utils


def process_num(line, state):
    val = int(line)
    all_numbers = state['all_numbers']
    recent_numbers = state['recent_numbers']
    preamble_length = state['preamble_length']

    recent_numbers.append(val)
    if len(recent_numbers) < (preamble_length + 1):
        all_numbers.append(val)
        return

    possible_sums = set()
    for i in range(preamble_length):
        for j in range(preamble_length):
            if i >= j:
                continue
            possible_sums.add(recent_numbers[i] + recent_numbers[j])

    if val in possible_sums:
        recent_numbers.pop(0)
        all_numbers.append(val)
        return

    print('Invalid number: %d' % val)
    recent_numbers.pop()
    for i in range(len(all_numbers)):
        thesum = all_numbers[i]
        #print('Check starting at %d: %d' % (i, thesum))
        j = i + 1
        while (thesum < val) and (j < len(all_numbers)):
            thesum += all_numbers[j]
            #print('...add %d: %d' % (j, thesum))
            j += 1
        if thesum != val:
            continue

        j -= 1
        sum_nums = all_numbers[i:(j+1)]
        print('Numbers from %d to %d add to %d: %r' % (i, j, val, sum_nums))
        sum_nums.sort()
        print('Min + max = %d' % (sum_nums[0] + sum_nums[-1]))
        break
            
    sys.exit(1)


if len(sys.argv) != 2:
    sys.stderr.write('Usage: sumbuddy preamble_length\n')
    sys.exit(1)

state = {'recent_numbers': [], 'all_numbers': [], 'preamble_length': int(sys.argv[1])}
utils.call_for_lines(process_num, state)
