#!/usr/bin/python3

import sys


class Point:
    def __init__(self, x, y, dot):
        self.x = x
        self.y = y
        self.dot = dot

    def __str__(self):
        if self.dot:
            return '#'
        else:
            return ' '

    def __hash__(self):
        return (self.x, self.y).__hash__()


class Paper:
    def __init__(self, width, height):
        self.rows = [[Point(x, y, False) for x in range(width)]
                     for y in range(height)]
        self.width = width
        self.height = height
        self.dots = set()

    def dot_at(self, x, y):
        point = self.point_at(x, y)
        point.dot = True
        self.dots.add(point)

    def fold(self, axis, pos):
        if axis == 'y':
            for y in range(pos+1, self.height):
                new_y = pos - (y - pos)
                old_row = self.rows[y]
                new_row = self.rows[new_y]
                for x in range(self.width):
                    point = old_row[x]
                    if not point.dot:
                        continue
                    #self.dots.remove(point)
                    new_point = new_row[x]
                    new_point.dot = True
                    #self.dots.add(new_point)
            self.height = self.height - pos
            if pos % 2 == 1:
                self.height -= 1
            #self.rows = self.rows[:self.height]
        else:
            for x in range(pos+1, self.width):
                new_x = pos - (x - pos)
                for y in range(self.height):
                    row = self.rows[y]
                    point = row[x]
                    if point.dot:
                        #self.dots.remove(point)
                        new_point = row[new_x]
                        new_point.dot = True
                        #self.dots.add(new_point)
            self.width = self.width - pos
            if pos % 2 == 0:
                self.width -= 1
            #for y, row in enumerate(self.rows):
            #    self.rows[y] = self.rows[y][:self.width]

    def point_at(self, x, y):
        return self.rows[y][x]

    def __str__(self):
        accum = []
        for y in range(self.height):
            row = self.rows[y]
            accum.append(''.join(list(map(lambda x: str(row[x]), range(self.width)))))
        return '\n'.join(accum)


max_x = 0
max_y = 0
dots = set()
while True:
    line = sys.stdin.readline().replace('\n', '')
    if line == '':
        break

    (x, y) = map(int, line.split(','))
    if x > max_x:
        max_x = x
    if y > max_y:
        max_y = y
    dots.add((x, y))

paper = Paper(max_x + 1, max_y + 1)
for x, y in dots:
    paper.dot_at(x, y)
print(paper)


while True:
    line = sys.stdin.readline().replace('\n', '')
    if line == '':
        break

    line = line.replace('fold along ', '')
    (axis, pos_s) = line.split('=')
    pos = int(pos_s)
    print('')
    print(f'Folding at {axis}={pos}')
    paper.fold(axis, pos)
    print(paper)
    print(f'{len(paper.dots)} dots visible')

marked_dots = 0
for y in range(paper.height):
    row = paper.rows[y]
    for x in range(paper.width):
        if row[x].dot:
            marked_dots += 1
print(marked_dots)
