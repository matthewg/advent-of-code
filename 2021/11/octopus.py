#!/usr/bin/python3

import sys


class Octopus:
    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.energy = energy

    def __str__(self):
        return f'({self.x},{self.y}={self.energy})'

    def __hash__(self):
        return (self.x, self.y).__hash__()

    def step(self):
        self.energy += 1

    def flashed(self):
        self.energy = 0


class Cavern:
    def __init__(self):
        self.rows = []
        self.width = 0
        self.height = 0

    def add_row(self, energies):
        y = len(self.rows)
        row = []
        self.rows.append(row)
        for x, energy in enumerate(energies):
            row.append(Octopus(x, y, energy))
        self.height += 1
        self.width = len(row)

    def adjacent(self, octopus):
        adj = []
        for delta_x in range(-1, 2):
            for delta_y in range(-1, 2):
                new_x = octopus.x + delta_x
                new_y = octopus.y + delta_y
                if new_x < 0 or new_y < 0 or new_x >= self.width or new_y >= self.height:
                    continue
                adj.append(self.octopus_at(new_x, new_y))
        return adj

    def octopus_at(self, x, y):
        return self.rows[y][x]

    def step(self):
        flashing_octopodes = set()
        for row in self.rows:
            for octopus in row:
                octopus.step()
                if octopus.energy > 9:
                    flashing_octopodes.add(octopus)

        flashed_octopodes = set()
        while True:
            need_flash = flashing_octopodes.difference(flashed_octopodes)
            if not need_flash:
                break
            for octopus in need_flash:
                flashed_octopodes.add(octopus)
                for adj_pus in self.adjacent(octopus):
                    adj_pus.step()
                    if adj_pus.energy > 9:
                        flashing_octopodes.add(adj_pus)
        for octopus in flashed_octopodes:
            octopus.flashed()
        return len(flashed_octopodes)


cavern = Cavern()
for line in sys.stdin.readlines():
    line = line.replace('\n', '')
    energies = map(int, line)
    cavern.add_row(energies)

# Day 1
#total_flashes = 0
#for _ in range(100):
#    total_flashes += cavern.step()
#print(total_flashes)

# Day 2
step = 0
while True:
    step += 1
    flashes = cavern.step()
    if flashes == cavern.width * cavern.height:
        print(step)
        break
