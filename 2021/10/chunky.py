#!/usr/bin/python3

import math
import sys


class NavSyntaxError(Exception):
    pass


class IncompleteLine(NavSyntaxError):
    def __init__(self, stack):
        self.stack = stack[:]


class CorruptLine(NavSyntaxError):
    def __init__(self, pos):
        self.pos = pos


def ParseChunks(line):
    stack = []
    for pos, char in enumerate(line):
        if char in ['(', '[', '{', '<']:
            stack.append(char)
        elif {'(': ')', '[': ']', '{': '}', '<': '>'}[stack.pop()] == char:
            pass
        else:
            raise CorruptLine(pos)

    if stack:
        raise IncompleteLine(stack)


part1_score = 0
part2_scores = []
for line in sys.stdin.readlines():
    line = line.replace('\n', '')
    try:
        chunks = ParseChunks(line)
    except IncompleteLine as e:
        this_score = 0
        e.stack.reverse()
        for char in e.stack:
            this_score *= 5
            this_score += {'(': 1, '[': 2, '{': 3, '<': 4}[char]
        part2_scores.append(this_score)
    except CorruptLine as e:
        part1_score += {')': 3, ']': 57, '}': 1197, '>': 25137}[line[e.pos]]
print(part1_score)
part2_scores.sort()
print(part2_scores[math.floor(len(part2_scores)/2)])
