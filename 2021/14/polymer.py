#!/usr/bin/python3

import collections
import sys


def PrintIt(char_freqs):
    freqpairs = list(char_freqs.items())
    freqpairs.sort(key=lambda freqpair: (freqpair[1], freqpair[0]))
    print(f'{freqpairs[-1]} - {freqpairs[0]} = {freqpairs[-1][1] - freqpairs[0][1]}')


def Iterate(pair_freqs, char_freqs, rules):
    new_pair_freqs = collections.defaultdict(lambda: 0)
    for pair in pair_freqs.keys():
        if pair_freqs[pair] == 0:
            continue
        new = rules.get(pair)
        if not new:
            new_pair_freqs[pair] += pair_freqs[pair]
            continue

        char_freqs[new] += pair_freqs[pair]
        new_pair_freqs[pair[0] + new] += pair_freqs[pair]
        new_pair_freqs[new + pair[1]] += pair_freqs[pair]
    return new_pair_freqs


polymer = sys.stdin.readline().replace('\n', '')
pair_freqs = collections.defaultdict(lambda: 0)
char_freqs = collections.defaultdict(lambda: 0)
char_freqs[polymer[0]] += 1
for i in range(1, len(polymer)):
    a = polymer[i-1]
    b = polymer[i]
    char_freqs[b] += 1
    pair = a + b
    pair_freqs[pair] += 1

sys.stdin.readline()

rules = {}
while True:
    line = sys.stdin.readline().replace('\n', '')
    if not line:
        break

    (src, dst) = line.split(' -> ')
    if src in rules:
        raise Exception(f'Polymer {src} already found in ruleset!')
    rules[src] = dst

for i in range(10):
    pair_freqs = Iterate(pair_freqs, char_freqs, rules)
PrintIt(char_freqs)

for i in range(30):
    pair_freqs = Iterate(pair_freqs, char_freqs, rules)
PrintIt(char_freqs)


