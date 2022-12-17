#!/usr/bin/python3
import re

print('graph {')
with open('input.txt') as f:
  for line in f:
    g = re.match('Valve (..) has flow rate=([0-9]+).*to valves? (.*)', line)
    valve = g.group(1)
    rate = g.group(2)
    tunnels = g.group(3).split(', ')
    print('{} [label="{}\\n{}"];'.format(valve, valve, rate))
    for tunnel in tunnels:
      print('{} -- {};'.format(valve, tunnel))
print('}')
