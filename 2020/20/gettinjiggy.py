#!/usr/bin/python3

import collections
import itertools
import heapq
import math
import random
import utils


class Border:
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3


class Orientation:
    def __init__(self, data, borders, oDesc):
        self.data = data
        self.borders = borders
        self.oDesc = oDesc


class Tile:
    def __init__(self, name, data):
        self.name = int(name)
        self.data = data
        self.width = len(self.data)
        self.height = len(self.data[0])

        print('Tile %d' % self.name)
        for row in self.data:
            print(row)
        
        self.orientations = [
            self._GetTransformedTile(flipX=flipX, flipY=flipY, rotateCW=rotateCW)
            for (flipX, flipY, rotateCW) in itertools.product((False, True), (False, True), (0, 1, 2, 3))
        ]

    def _GetTransformedTile(self, flipX=False, flipY=False, rotateCW=0):
        data = self.data[:]
        if flipX:
            data = [''.join([c for c in reversed(row)])
                    for row in data]
        if flipY:
            data.reverse()
        for _ in range(rotateCW):
            newdata = [['' for _ in range(self.width)]
                       for _ in range(self.height)]
            for y in range(self.height):
                newRow = []
                for x in range(self.width):
                    newX = self.height - y - 1
                    newY = x
                    newdata[newY][newX] = data[y][x]
            data = [''.join(row) for row in newdata]

        print('===== Orient (flipX=%r, flipY=%r, rotateCW=%d) =====' % (flipX, flipY, rotateCW))
        for row in data:
            print(row)
        return Orientation(
            data,
            [
                data[0],
                ''.join([row[-1] for row in data]),
                data[-1],
                ''.join([row[0] for row in data]),
            ],
            (flipX, flipX, rotateCW))


def ParseTile(tile_lines, state):
    #print('ParseTile(%r)' % tile_lines)
    name = tile_lines.pop(0).split(' ')[1].replace(':', '')
    data = tile_lines
    #print('Got tile %r with data %r' % (name, data))
    state['tiles'].append(Tile(name, data))


class State:
    def __init__(self):
        self.arrangement = None
        self.unplacedTiles = None
        self.tileOrientations = None
        self.successorMoves = set()
        self.lastX = -1
        self.lastY = -1
        self.lastTile = None
        self.lastODesc = None

    def __lt__(self, other):
        return len(self.unplacedTiles) < len(other.unplacedTiles)
        
    @classmethod
    def NewState(clazz, gridsize, tiles):
        self = clazz()
        self.arrangement = [[None for _ in range(gridsize)] for _ in range(gridsize)]
        self.unplacedTiles = set(tiles)
        self.tileOrientations = {}
        return self

    @classmethod
    def CopyState(clazz, other):
        self = clazz()
        self.arrangement = [other.arrangement[x][:] for x in range(len(other.arrangement))]
        self.unplacedTiles = set(other.unplacedTiles)
        self.tileOrientations = dict(other.tileOrientations)
        return self

    def PlaceTile(self, tile, orientation, x, y):
        if tile not in self.unplacedTiles:
            raise Exception('Tile already placed')
        self.arrangement[x][y] = tile
        self.tileOrientations[tile] = orientation
        self.unplacedTiles.remove(tile)
        self.lastX = x
        self.lastY = y
        self.lastTile = tile
        self.lastOrientation = orientation


def PrintFoo(state, cameFrom, depth=0):
    depthStr = ' ' * (depth*2)
    if not state.lastTile:
        print('%sInitial state' % depthStr)
        return

    tile = state.lastTile
    tileSize = len(tile.data)
    gridSize = len(state.arrangement)
    midStr = ' ' * (tileSize - 2)
    for x in range(gridSize):
        for y in range(gridSize):
            if not state.arrangement[x][y]:
                continue
            tile = state.arrangement[x][y]
            print('%s(%d, %d): Tile %d in orientation %r' % (depthStr, x, y, tile.name, state.tileOrientations[tile].oDesc))
    #print('%sPlaced at %d,%d (%d remaining):' % (depthStr, state.lastX, state.lastY, len(state.unplacedTiles)))
    for gridRow in range(gridSize):
        for tileRow in range(tileSize):
            tiles = [state.arrangement[gridCol][gridRow] for gridCol in range(gridSize)]
            rowData = [state.tileOrientations[tile].data[tileRow]
                       if tile else 'x' * tileSize
                       for tile in tiles]
            print('%s%s' % (depthStr, ' '.join(rowData)))
        print('')
    #borders = state.tileOrientations[state.lastTile]
    #print('%s%s' % (depthStr, borders[Border.TOP]))
    #for i in range(1, len(tile.data) - 1):
    #    print('%s%s%s%s' % (depthStr, borders[Border.LEFT][i], midStr, borders[Border.RIGHT][i]))
    #print('%s%s' % (depthStr, borders[Border.BOTTOM]))
    #prevState = cameFrom[state]
    #if prevState:
    #    PrintFoo(prevState, cameFrom, depth+1)


def FindNeighbors(x, y, gridSize):
    ret = []
    for (dX, dY, ourBorder, theirBorder) in ((-1, 0, Border.LEFT, Border.RIGHT),
                                             (1, 0, Border.RIGHT, Border.LEFT),
                                             (0, -1, Border.TOP, Border.BOTTOM),
                                             (0, 1, Border.BOTTOM, Border.TOP)):
        nX = x + dX
        nY = y + dY
        if nX < 0 or nY < 0 or nX >= gridSize or nY >= gridSize:
            continue
        ret.append((nX, nY, ourBorder, theirBorder))
    return ret


def Arrange(tiles):
    random.shuffle(tiles)
    gridsize = math.sqrt(len(tiles))
    if gridsize != int(gridsize):
        raise Exception('Not a square')
    gridsize = int(gridsize)
    print('Grid size: %d' % gridsize)

    initialState = State.NewState(gridsize, tiles)

    cameFrom = {}
    openSet = []
    for initialTile in tiles:
        for initialOrientation in initialTile.orientations:
            state = State.CopyState(initialState)
            state.PlaceTile(initialTile, initialOrientation, 0, 0)
            heapq.heappush(openSet, state)
            cameFrom[state] = initialState

    print('Looking through possibilities, starting with %d' % len(openSet))
    step = 0
    while openSet:
        state = heapq.heappop(openSet)
        if step % 100 == 0:
            print('Step %d: Remaining tiles: %d (%d possibilities)' % (step, len(state.unplacedTiles), len(openSet)))
        step += 1
        #print('This state: placed %d at %d,%d in %r' % (state.lastTile.name, state.lastX, state.lastY, state.lastODesc))
        if not state.unplacedTiles:
            return (state.arrangement, state, cameFrom)

        for x in range(gridsize):
            for y in range(gridsize):
                if not state.arrangement[x][y]:
                    continue

                for neighborData in FindNeighbors(x, y, gridsize):
                    nX = neighborData[0]
                    nY = neighborData[1]
                    if state.arrangement[nX][nY]:
                        continue

                    #print('Found an open neighbor for (%d, %d) => (%d, %d)' % (x, y, nX, nY))
                    foundOpenNeighbor = True
                    for nTile in state.unplacedTiles:
                        for nTileOrientation in nTile.orientations:
                            fitsExistingNeighbors = True
                            for (existingX, existingY, nTileBorder, existingBorder) in FindNeighbors(nX, nY, gridsize):
                                existingTile = state.arrangement[existingX][existingY]
                                if not existingTile:
                                    continue
                                existingOrientation = state.tileOrientations[existingTile]
                                if nTileOrientation.borders[nTileBorder] != existingOrientation.borders[existingBorder]:
                                    #print('Rejecting placement of %d at %d,%d with %r due to neighbor %d,%d: %r != %r' % (
                                    #    nTile.name, nX, nY, oDesc, existingX, existingY, nTileOrientation[nTileBorder], existingOrientation[existingBorder]))
                                    fitsExistingNeighbors = False
                                    break
                            if not fitsExistingNeighbors:
                                continue
                            nextState = State.CopyState(state)
                            nextState.PlaceTile(nTile, nTileOrientation, nX, nY)
                            cameFrom[nextState] = state
                            #PrintFoo(nextState, cameFrom)
                            heapq.heappush(openSet, nextState)
    raise Exception('Did not find a valid arrangement')


state = {'tiles': []}
utils.call_for_records(ParseTile, state)
(arrangement, state, cameFrom) = Arrange(state['tiles'])
#while state:
#    if state.lastTile:
#        #print('Placed %d at %d,%d with orientation %s' % (state.lastTile.name, state.lastX, state.lastY, state.lastODesc))
#        state = cameFrom[state]
#    else:
#        state = None
PrintFoo(state, cameFrom)
print(arrangement[0][0].name * arrangement[0][-1].name * arrangement[-1][0].name * arrangement[-1][-1].name)
