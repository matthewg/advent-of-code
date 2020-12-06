#!/usr/bin/python3

import collections
import sys

def NewAnswers():
    return collections.defaultdict(lambda: 0)
answers = NewAnswers()

totalAnswersAny = 0
totalAnswersEvery = 0
done = False
groupSize = 0
while True:
    line = sys.stdin.readline()
    if line:
        line = line.replace('\n', '')
        if line:
            groupSize += 1
    else:
        done = True

    for c in line:
        answers[c] += 1

    if not line:
        totalAnswersAny += len(answers)
        totalAnswersEvery += len([c for c in answers.keys() if answers[c] == groupSize])
        answers = NewAnswers()
        groupSize = 0
    if done:
        break
print('Anyone: %d' % totalAnswersAny)
print('Everyone: %d' % totalAnswersEvery)
