#!/usr/bin/python3

import sys

minSeatId = 9999999
maxSeatId = 0
seenSeats = set()

for line in sys.stdin.readlines():
    line = line.replace('\n', '')

    minRow = 0
    maxRow = 128
    minCol = 0
    maxCol = 8
    for char in line:
        if char == 'F':
            maxRow -= (maxRow - minRow) / 2
        elif char == 'B':
            minRow += (maxRow - minRow) / 2
        elif char == 'L':
            maxCol -= (maxCol - minCol) / 2
        elif char == 'R':
            minCol += (maxCol - minCol) / 2
    if maxRow - 1 != minRow or maxCol - 1 != minCol:
        sys.stderr.write('Did not converge for %s: %d/%d/%d/%d\n' % (line, minRow, maxRow, minCol, maxCol))
        sys.exit(1)

    seatId = int(minRow * 8 + minCol)
    seenSeats.add(seatId)
    print('%s: row %d, col %d, seat %d' % (line, minRow, minCol, seatId))

    if seatId > maxSeatId:
        maxSeatId = seatId
    if seatId < minSeatId:
        minSeatId = seatId
print('Max seat: %d' % maxSeatId)

for seat in range(minSeatId, maxSeatId):
    if (seat - 1) in seenSeats and (seat + 1) in seenSeats and seat not in seenSeats:
        print('Your seat is %d' % seat)
