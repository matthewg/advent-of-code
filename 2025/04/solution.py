#!/usr/bin/python3
import utils

g = utils.Grid(lambda x: x == '@')
g.Parse({})

can_access = 0
for c in g:
    if not c.value:
        continue
    adj_count = 0
    for adj in g.AdjacentCells(c, True):
        if adj.value:
            adj_count += 1
    if adj_count < 4:
        can_access += 1
print(can_access)

can_access = 0
prev_access = -1
while can_access != prev_access:
    prev_access = can_access
    for c in g:
        if not c.value:
            continue
        adj_count = 0
        for adj in g.AdjacentCells(c, True):
            if adj.value:
                adj_count += 1
        if adj_count < 4:
            can_access += 1
            c.value = False
print(can_access)
