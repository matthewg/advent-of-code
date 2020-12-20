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

        #print('Tile %d' % self.name)
        #for row in self.data:
        #    print(row)
        
        self.orientations = [
            self._GetTransformedTile(flip=flip, rotateCW=rotateCW)
            for (flip, rotateCW) in itertools.product((0, 1, 2), (0, 1, 2, 3))
        ]

    def _GetTransformedTile(self, flip, rotateCW):
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

        #print('===== Orient (flipX=%r, flipY=%r, rotateCW=%d) =====' % (flipX, flipY, rotateCW))
        #for row in data:
        #    print(row)
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
        self.lastDir = None

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

    def PlaceTile(self, tile, orientation, x, y, direction):
        if tile not in self.unplacedTiles:
            raise Exception('Tile already placed')
        self.arrangement[x][y] = tile
        self.tileOrientations[tile] = orientation
        self.unplacedTiles.remove(tile)
        self.lastX = x
        self.lastY = y
        self.lastTile = tile
        self.lastOrientation = orientation
        self.lastDir = direction


def PrintFoo(state, cameFrom, depth=0):
    depthStr = ' ' * (depth*2)
    if not state or not state.lastTile:
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


def FindEdgeCandidates(edge, tiles):
    edgeOptions = collections.defaultdict(lambda: collections.defaultdict(list))
    for tile in tiles:
        for orientation in tile.orientations:
            edgeOptions[orientation.borders[edge]][tile].append(orientation)
    #print('Potential edge candidates for %d:' % edge)
    #for (border, options) in edgeOptions.items():
    #    print('  %r:' % border)
    #    for (tile, orientation) in options:
    #        print('    %d in %r' % (tile.name, orientation.oDesc))

    optionsForEdge = collections.defaultdict(list)
    for (border, tiles) in edgeOptions.items():
        if len(tiles) > 1:
            continue
        for (tile, orientations) in tiles.items():
            optionsForEdge[tile].extend(orientations)
    return (edge, optionsForEdge)


def Arrange(tiles, edgeCandidates, cornerCandidates):
    random.shuffle(tiles)
    gridsize = math.sqrt(len(tiles))
    if gridsize != int(gridsize):
        raise Exception('Not a square')
    gridsize = int(gridsize)
    print('Grid size: %d' % gridsize)

    initialState = State.NewState(gridsize, tiles)

    cameFrom = {}
    openSet = []
    for (initialTile, initialOrientations) in cornerCandidates.items():
        for initialOrientation in initialOrientations:
            state = State.CopyState(initialState)
            state.PlaceTile(initialTile, initialOrientation, 0, 0, (1, 0))
            heapq.heappush(openSet, state)
            cameFrom[state] = initialState

    print('Looking through possibilities, starting with %d' % len(openSet))
    step = 0
    while openSet:
        state = heapq.heappop(openSet)
        if step % 100 == 0:
            print('Step %d: Remaining tiles: %d (%d possibilities)' % (step, len(state.unplacedTiles), len(openSet)))
        step += 1
        #print('This state: placed %d at %d,%d in %r' % (state.lastTile.name, state.lastX, state.lastY, state.lastOrientation.oDesc))
        #PrintFoo(state, cameFrom)
        if not state.unplacedTiles:
            return (state.arrangement, state, cameFrom)

        lastX = state.lastX
        lastY = state.lastY
        lastDir = state.lastDir
        nextDir = lastDir

        # Place in a clockwise spiral so that we get the edges first
        #print('Looking for next placement from %d,%d : %r' % (lastX, lastY, lastDir))
        while True:
            nX = lastX + nextDir[0]
            nY = lastY + nextDir[1]
            #print('Trying (%d,%d)' % nextDir)
            if (nX + 1) > gridsize:
                #print('Would fall off right')
                pass
            elif (nY + 1) > gridsize:
                #print('Would fall off bottom')
                pass
            elif nX < 0:
                #print('Would fall off left')
                pass
            elif nY < 0:
                #print('Would fall off top')
                pass
            elif state.arrangement[nX][nY]:
                #print('Occupied')
                pass
            else:
                break
            
            if nextDir == (1, 0):
                nextDir = (0, 1)
            elif nextDir == (0, 1):
                nextDir = (-1, 0)
            elif nextDir == (-1, 0):
                nextDir = (0, -1)
            elif nextDir == (0, -1):
                nextDir = (1, 0)

            if lastDir == nextDir:
                raise Exception('Did not find valid next tile, but unplaced tiles remain')

        onEdges = []
        if nX == 0:
            onEdges.append(Border.LEFT)
        elif (nX+1) >= gridsize:
            onEdges.append(Border.RIGHT)

        if nY == 0:
            onEdges.append(Border.TOP)
        elif (nY+1) >= gridsize:
            onEdges.append(Border.BOTTOM)
    
        #print('Found an open neighbor for (%d, %d) => (%d, %d)' % (lastX, lastY, nX, nY))
        for nTile in state.unplacedTiles:

            # Place corner candidates in corners, and don't place them anywhere else
            isCornerCandidate = nTile in cornerCandidates
            if len(onEdges) < 2 and isCornerCandidate:
                #print('Rejecting placement of %d at %d,%d because reserving it for corners' % (nTile.name, nX, nY))
                continue
            elif len(onEdges) == 2 and not isCornerCandidate:
                #print('Rejecting placement of %d at %d,%d because need corner candidate' % (nTile.name, nX, nY))
                continue
            
            for nTileOrientation in nTile.orientations:
                matchesEdgeCandidates = True

                for edge in onEdges:
                    if nTile not in edgeCandidates[edge] or nTileOrientation not in edgeCandidates[edge][nTile]:
                        matchesEdgeCandidates = False
                        break
                if not matchesEdgeCandidates:
                    #print('Rejecting placement of %d in %r at %d,%d due to edge candidates %r' % (nTile.name, nTileOrientation.oDesc, nX, nY, onEdges))
                    continue

                fitsExistingNeighbors = True
                for (existingX, existingY, nTileBorder, existingBorder) in FindNeighbors(nX, nY, gridsize):
                    existingTile = state.arrangement[existingX][existingY]
                    if not existingTile:
                        continue
                    existingOrientation = state.tileOrientations[existingTile]
                    if nTileOrientation.borders[nTileBorder] != existingOrientation.borders[existingBorder]:
                        #print('Rejecting placement of %d at %d,%d with %r due to neighbor %d,%d' % (
                        #    nTile.name, nX, nY, nTileOrientation.oDesc, existingX, existingY))
                        fitsExistingNeighbors = False
                        break
                if not fitsExistingNeighbors:
                    continue
                #print('Ok to place %d at %d,%d with %r' % (nTile.name, nX, nY, nTileOrientation.oDesc))
                nextState = State.CopyState(state)
                nextState.PlaceTile(nTile, nTileOrientation, nX, nY, nextDir)
                cameFrom[nextState] = state
                #PrintFoo(nextState, cameFrom)
                heapq.heappush(openSet, nextState)
    raise Exception('Did not find a valid arrangement')


state = {'tiles': []}
utils.call_for_records(ParseTile, state)

edgeCandidates = dict(FindEdgeCandidates(edge, state['tiles'])
                      for edge in (Border.TOP, Border.RIGHT, Border.BOTTOM, Border.LEFT))
for edge in (Border.TOP, Border.RIGHT, Border.BOTTOM, Border.LEFT):
    print('Found edge candidates for %r:' % edge)
    for (tile, orientations) in edgeCandidates[edge].items():
        for orientation in orientations:
            print('  Tile %d in orientation %r' % (tile.name, orientation.oDesc))
cornerCandidates = collections.defaultdict(list)
corner = (Border.TOP, Border.LEFT)
print('Found candidates for corner:')
for (tile, orientations) in edgeCandidates[corner[0]].items():
    for orientation in orientations:
        if tile in edgeCandidates[corner[1]] and orientation in edgeCandidates[corner[1]][tile]:
            cornerCandidates[tile].append(orientation)
            print('  Tile %d in orientation %r' % (tile.name, orientation.oDesc))
part1Answer = 1
for cornerTile in cornerCandidates.keys():
    part1Answer *= cornerTile.name
print('Part 1 answer: %d' % part1Answer)

(arrangement, state, cameFrom) = Arrange(state['tiles'], edgeCandidates, cornerCandidates)
PrintFoo(state, cameFrom)

#while state:
#    if state.lastTile:
#        #print('Placed %d at %d,%d with orientation %s' % (state.lastTile.name, state.lastX, state.lastY, state.lastODesc))
#        state = cameFrom[state]
#    else:
#        state = None
#PrintFoo(state, cameFrom)
