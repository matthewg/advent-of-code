#!/usr/bin/python3
import collections
import re
import utils


def PlayGame(line, state, _):
    card = re.split(r': +', line)
    #print(card[0])
    card_no = int((re.split(r' +', card[0])[1]))
    game = card[1]
    fields = re.split(r' +[|] +', game)
    win = set([int(x) for x in re.split(r' +', fields[0])])
    have = [int(x) for x in re.split(r' +', fields[1])]

    sum = 0
    num_matches = 0
    for num in have:
        if num in win:
            num_matches += 1
            if not sum:
                sum = 1
            else:
                sum *= 2
            #print(f'  match @ {num}, new sum {sum}')
    #print(f'  Total: {sum}')
    state['points_by_card'].append(num_matches)
    state['sum'] += sum


state = {'sum': 0, 'points_by_card': [], 'card_counts': collections.defaultdict(lambda: 1)}
utils.call_for_lines(PlayGame, state)
print(state['sum'])

total_cards = 0
for i, points in enumerate(state['points_by_card']):
    print(f'At {i} have {points}')
    total_cards += 1
    for point in range(points):
        total_cards += state['points_by_card'][i+point]
print(total_cards)
