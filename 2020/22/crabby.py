#!/usr/bin/python3

import sys


def deckscore(deck):
    score = 0
    cardno = 0
    for card in reversed(deck):
        cardno += 1
        score += card * cardno
    return score


data_str = sys.stdin.read()
(deck1, deck2) = data_str.split('\n\n')
deck1 = [int(x) for x in deck1.replace('Player 1:\n', '').split('\n') if x]
deck2 = [int(x) for x in deck2.replace('Player 2:\n', '').split('\n') if x]


round = 0
while deck1 and deck2:
    round += 1
    card1 = deck1.pop(0)
    card2 = deck2.pop(0)
    if card1 > card2:
        deck1.append(card1)
        deck1.append(card2)
    elif card2 > card1:
        deck2.append(card2)
        deck2.append(card1)
    else:
        raise Exception('card1 == card2')

print('After %d rounds...' % round)
if deck1:
    print('deck1 wins with a score of %d' % deckscore(deck1))
else:
    print('deck2 wins with a score of %d' % deckscore(deck2))
