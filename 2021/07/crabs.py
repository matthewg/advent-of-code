#!/usr/bin/python3

import functools
import sys


crab_h = list(map(int, sys.stdin.readline().replace('\n', '').split(',')))

min_h = min(crab_h)
max_h = max(crab_h)
fuel_costs_1 = []
fuel_costs_2 = []

crab_costs = []
for h in range(max_h - min_h + 1):
    if crab_costs:
        crab_costs.append(crab_costs[-1] + h)
    else:
        crab_costs.append(0)

for h in range(min_h, max_h+1):
    fuel_cost_1 = functools.reduce(lambda a,b: a + b, map(lambda crab: abs(crab - h), crab_h))
    fuel_costs_1.append((h, fuel_cost_1))

    movements = list(map(lambda crab: crab_costs[abs(crab - h)], crab_h))
    #print(f'Aligning at {h}:')
    #for movement in movements:
    #   print(f'...{movement}') 
    fuel_cost_2 = functools.reduce(lambda a,b: a + b, movements)
    fuel_costs_2.append((h, fuel_cost_2))
    #print(f'...Aligning at {h} costs {fuel_cost_2}')
    
fuel_costs_1.sort(key=lambda cost: cost[1])
print(f'Day 1: Aligning at {fuel_costs_1[0][0]} costs {fuel_costs_1[0][1]}.')
fuel_costs_2.sort(key=lambda cost: cost[1])
print(f'Day 2: Aligning at {fuel_costs_2[0][0]} costs {fuel_costs_2[0][1]}.')
