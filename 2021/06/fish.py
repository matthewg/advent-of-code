#!/usr/bin/python3

from functools import reduce
import sys
import utils


class Fish:
    def __init__(self, days_until_spawn=None, parent_generation=0):
        self.parent_generation = parent_generation
        if days_until_spawn is None:
            self.days_until_spawn = self.max_age()
        else:
            self.days_until_spawn = days_until_spawn

    def max_age(self):
        return 6 + 2 * self.parent_generation

    def age(self):
        if self.days_until_spawn == 0:
            self.parent_generation=0
            self.days_until_spawn = self.max_age()
            return Fish(parent_generation=1)
        else:
            self.days_until_spawn -= 1
            return None

    def __str__(self):
        return str(self.days_until_spawn)


oldfish_by_day = [0, 0, 0, 0, 0, 0, 0, 0, 0]
newfish_by_day = [0, 0, 0, 0, 0, 0, 0, 0, 0]
for fish in sys.stdin.readline().replace('\n', '').split(','):
    oldfish_by_day[int(fish)] += 1

for day in range(257):
    print('Day: {}'.format(day))
    total_fish = reduce(lambda a,b: a + b, oldfish_by_day) + reduce(lambda a, b: a + b, newfish_by_day)
    if day in (80, 256):
        print('On day {}, {} fish'.format(day, total_fish))
        #print('..old fish: {}'.format(', '.join(map(str, oldfish_by_day))))
        #print('..new fish: {}'.format(', '.join(map(str, newfish_by_day))))
        if day == 256:
            break

    oldfish = oldfish_by_day[:]
    newfish = newfish_by_day[:]
    newfish_by_day[8] = oldfish[0] + newfish[0]
    newfish_by_day[7] = newfish[8]
    newfish_by_day[6] = newfish[7]
    newfish_by_day[5] = newfish[6]
    newfish_by_day[4] = newfish[5]
    newfish_by_day[3] = newfish[4]
    newfish_by_day[2] = newfish[3]
    newfish_by_day[1] = newfish[2]
    newfish_by_day[0] = newfish[1]
    oldfish_by_day[6] = newfish[0] + oldfish[0]
    oldfish_by_day[5] = oldfish[6]
    oldfish_by_day[4] = oldfish[5]
    oldfish_by_day[3] = oldfish[4]
    oldfish_by_day[2] = oldfish[3]
    oldfish_by_day[1] = oldfish[2]
    oldfish_by_day[0] = oldfish[1]
