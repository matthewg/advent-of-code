#!/usr/bin/python3

import collections
import utils


def find_set_bits(line, state, _):
    state['all_numbers'].append(line)
    for idx, bit in enumerate(line):
        state['bit_count'][idx][int(bit)] += 1


def find_value(state, most_common):
    candidates = state['all_numbers'][:]
    bit_idx = 0
    while len(candidates) > 1:
        bit_counts = [0, 0]
        for candidate in candidates:
            bit_counts[int(candidate[bit_idx])] += 1

        #print('Bit count for bit_idx: {}'.format(bit_counts))
        if most_common:
            if bit_counts[1] >= bit_counts[0]:
                desired_bit = '1'
            else:
                desired_bit = '0'
        else:
            if bit_counts[0] <= bit_counts[1]:
                desired_bit = '0'
            else:
                desired_bit = '1'
        #print('bit_idx={}, desired_bit={} (MC={})'.format(bit_idx, desired_bit, most_common))
        
        new_candidates = []
        for candidate in candidates:
            #print('Candidate {} has value {} (?= {})'.format(''.join(candidate), candidate[bit_idx], desired_bit))
            if candidate[bit_idx] == desired_bit:
                new_candidates.append(candidate)
        candidates = new_candidates
        bit_idx += 1
    #print('Found value: {}'.format(''.join(candidates[0])))
    return ''.join(candidates[0])
    

state = {
    'all_numbers': [],
    'bit_count': collections.defaultdict(lambda: [0, 0]),
}
utils.call_for_lines(find_set_bits, state)

# Day 1
gamma_rate = []
epsilon_rate = []
for bit in state['bit_count'].values():
    if bit[0] > bit[1]:
        gamma_rate.append('0')
        epsilon_rate.append('1')
    else:
        gamma_rate.append('1')
        epsilon_rate.append('0')
gamma_rate = ''.join(gamma_rate)
gamma_num = int(gamma_rate, base=2)
epsilon_rate = ''.join(epsilon_rate)
epsilon_num = int(epsilon_rate, base=2)
print('Gamma rate: {} -> {}'.format(gamma_rate, gamma_num))
print('Epsilon rate: {} -> {}'.format(epsilon_rate, epsilon_num))
print('Gamma * epsilon: {}'.format(gamma_num * epsilon_num))


# Day 2
o2_value = ''.join(find_value(state, most_common=True))
co2_value = ''.join(find_value(state, most_common=False))
o2_num = int(o2_value, base=2)
co2_num = int(co2_value, base=2)
print('O2: {} -> {}'.format(o2_value, o2_num))
print('CO2: {} -> {}'.format(co2_value, co2_num))
print('O2 * CO2: {}'.format(o2_num * co2_num))
