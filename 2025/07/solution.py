#!/usr/bin/python3
import utils

g = utils.Grid(lambda x: x)
g.Parse({})

start = None
for c in g.rows[0]:
    if c.value == 'S':
        start = c
        break

beams1 = set([start.col])
beams2 = {start.col: 1}

splits1 = 0
splits2 = 1
for row_idx, r in enumerate(g.rows[1:], 1):
    new_beams1 = set()
    for beam in beams1:
        if r[beam].value == '^':
            splits1 += 1
            new_beams1.add(beam - 1)
            new_beams1.add(beam + 1)
        else:
            new_beams1.add(beam)
    beams1 = new_beams1

    new_beams2 = {}
    for beam, count in beams2.items():
        if r[beam].value == '^':
            splits2 += count
            new_beams2[beam - 1] = new_beams2.get(beam - 1, 0) + count
            new_beams2[beam + 1] = new_beams2.get(beam + 1, 0) + count
        else:
            new_beams2[beam] = new_beams2.get(beam, 0) + count
    beams2 = new_beams2

print(splits1)
print(splits2)
