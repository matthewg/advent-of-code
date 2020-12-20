#!/usr/bin/python3

import itertools
import sys


def TransformBoard(board, flip, rotate):
    if flip == 0:
        flipX = False
        flipY = False
    elif flip == 1:
        flipX = True
        flipY = False
    elif flip == 2:
        flipX = False
        flipY = True
    else:
        raise Exception('Unsupported flip: %r' % flip)

    height = len(board)
    width = len(board[0])
    
    board = [row[:] for row in board]
    if flipX:
        board = [[c for c in reversed(row)]
                 for row in board]
    if flipY:
        board.reverse()
    for _ in range(rotate):
        newWidth = height
        newHeight = width
        newBoard = [['' for _ in range(newWidth)]
                    for _ in range(newHeight)]
        for y in range(height):
            newRow = []
            for x in range(width):
                newX = height - y - 1
                newY = x
                newBoard[newY][newX] = board[y][x]
        board = newBoard
        width = newWidth
        height = newHeight
    return board


monster = [
    list('                  # '),
    list('#    ##    ##    ###'),
    list(' #  #  #  #  #  #   '),
]

initialBoard = []
skipNextLine = True
for line in sys.stdin.readlines():
    line = line.replace('\n', '')
    if not line:
        if initialBoard:
            initialBoard.pop()
        skipNextLine = True
        continue
    if skipNextLine:
        skipNextLine = False
        continue

    initialBoard.append([line[i] for i in range(len(line))
                         if line[i] != ' ' and i > 0 and (i+1) < len(line) and line[i+1] != ' ' and line[i-1] != ' '])
initialBoard.pop()


#for row in initialBoard:
#    print(''.join(row))
#sys.exit(0)
    
boards = [
    TransformBoard(initialBoard, flip, rotate)
    for (flip, rotate) in itertools.product((0, 1, 2), (0, 1, 2, 3))]

monsterCount = 0
monsterHeight = len(monster)
monsterWidth = len(monster[0])
for board in boards:
    #print('Looking for monster on board:')
    #for row in board:
    #    print(''.join(row))

    height = len(board)
    width = len(board[0])
    for y in range(height):
        if (y + monsterHeight) >= height:
            #print('y=%d is too close to bottom' % y)
            continue
        
        for x in range(width):
            if (x + monsterWidth) >= width:
                #print('x=%d is too close to right' % x)
                continue

            foundMonster = True
            #print('Looking for monster at %d,%d' % (x,y))
            for dY in range(monsterHeight):
                for dX in range(monsterWidth):
                    if monster[dY][dX] != '#':
                        continue
                    if board[y+dY][x+dX] != '#':
                        #print('No monster match at %d,%d' % (x+dX, y+dY))
                        foundMonster = False
                        break
                if not foundMonster:
                    break
            if foundMonster:
                # We found a match! We found a monster match!
                monsterCount += 1
                for dY in range(monsterHeight):
                    for dX in range(monsterWidth):
                        if monster[dY][dX] != '#':
                            continue
                        board[y+dY][x+dX] = 'O'
    if monsterCount:
        break
print('Found monsters: %d' % monsterCount)

roughness = 0
print('Board after finding monsters:')
for row in board:
    print(''.join(row))
    for col in row:
        if col == '#':
            roughness += 1
print('Roughness: %d' % roughness)
