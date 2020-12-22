#!/usr/bin/python3

import collections
import sys


class Winner:
    DECK1 = 1
    DECK2 = 2


Result = collections.namedtuple('Result', ['winner', 'deck1', 'deck2'])


def DeckScore(deck):
    score = 0
    cardno = 0
    for card in reversed(deck):
        cardno += 1
        score += card * cardno
    return score


def Play(deck1, deck2, depth=1):
    prev_decks = set()

    round = 0
    while deck1 and deck2:
        #print('R=%d. round=%d, len1=%d, len2=%d' % (depth, round, len(deck1), len(deck2)))
        decks = (tuple(deck1), tuple(deck2))
        if decks in prev_decks:
            return Result(Winner.DECK1, deck1, deck2)
        prev_decks.add(decks)
        
        round += 1
        card1 = deck1.pop(0)
        card2 = deck2.pop(0)
        if len(deck1) >= card1 and len(deck2) >= card2:
            winner = Play(deck1[:card1], deck2[:card2], depth+1).winner
        elif card1 > card2:
            winner = Winner.DECK1
        elif card2 > card1:
            winner = Winner.DECK2
        else:
            raise Exception('card1 == card2')

        if winner == Winner.DECK1:
            deck1.append(card1)
            deck1.append(card2)
        elif winner == Winner.DECK2:
            deck2.append(card2)
            deck2.append(card1)
        else:
            raise Exception('Unexpected winner: %r' % winner)
    return Result(Winner.DECK1 if deck1 else Winner.DECK2, deck1, deck2)
    
            
data_str = sys.stdin.read()
(deck1, deck2) = data_str.split('\n\n')
deck1 = [int(x) for x in deck1.replace('Player 1:\n', '').split('\n') if x]
deck2 = [int(x) for x in deck2.replace('Player 2:\n', '').split('\n') if x]

result = Play(deck1, deck2)

if result.winner == Winner.DECK1:
    print('deck1 wins with a score of %d' % DeckScore(result.deck1))
else:
    print('deck2 wins with a score of %d' % DeckScore(result.deck2))
