#!/usr/bin/python3
import utils


"""
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
12, 13, 14
"""

def is_possible(s, state, line_idx):
    toks = s.split(': ')

    game_s = toks[0]
    game_idx = int(game_s.split(' ')[1])

    games = toks[1].split('; ')

    is_possible = True
    min_vals = {'red': 0, 'green': 0, 'blue': 0}
    for game in games:
        draws = game.split(', ')
        vals = {'red': 0, 'green': 0, 'blue': 0}
        for draw in draws:
            d_toks = draw.split(' ')
            val = int(d_toks[0])
            color = d_toks[1]
            vals[color] = val
            if val > min_vals[color]:
                min_vals[color] = val
        if vals['red'] > 12 or vals['green'] > 13 or vals['blue'] > 14:
            #print(f'Game {game_idx} not possible: {vals}: {toks[1]}')
            is_possible = False
    if is_possible:
        #print(f'Game {game_idx} possible:')
        #for game in games:
        #    print(f'    {game}')
        state['sum'] += game_idx
    power = min_vals['red'] * min_vals['green'] * min_vals['blue']
    state['power'] += power

state = {'sum': 0, 'power': 0}
utils.call_for_lines(is_possible, state)
print(state['sum'])
print(state['power'])
