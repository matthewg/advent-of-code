#!/usr/bin/python3

class State:
    def __init__(self, velX, velY, minX, minY, maxX, maxY):
        self.pos = [0, 0]
        self.vel = [velX, velY]
        self.initialVel = list(self.vel)
        self.targMin = [minX, minY]
        self.targMax = [maxX, maxY]


    def Step(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.vel[1] -= 1
        if self.vel[0] > 0:
            self.vel[0] -= 1
        elif self.vel[0] < 0:
            self.vel[0] += 1


    def InTarget(self):
        return (self.pos[0] >= self.targMin[0] and self.pos[0] <= self.targMax[0] and
                self.pos[1] >= self.targMin[1] and self.pos[1] <= self.targMax[1])


    def Overshot(self):
        return self.pos[0] > self.targMax[0] and self.pos[1] < self.targMin[1]


    def TryIt(self):
        prevPos = None
        stepCount = 0
        maxY = 0
        while True:
            if self.InTarget():
                print(f'After step {stepCount}, position {self.pos} is in target. maxY={maxY}, initial={self.initialVel}')
                return maxY
            elif self.Overshot():
                #print(f'After step {stepCount}, we overshot target: {prevPos} -> {self.pos}')
                return None
            elif self.vel[0] == 0 and ((self.pos[0] < self.targMin[0] or self.pos[0] > self.targMax[0])
                                       or self.pos[1] < self.targMin[1]):
                #print(f'After step {stepCount}, we reached 0 X velocity: {self.pos}')
                return None
            prevPos = list(self.pos)
            stepCount += 1
            self.Step()
            #print(f'{self.pos} / {self.vel}')
            if self.pos[1] > maxY:
                maxY = self.pos[1]


maxMaxY = None
totalWinners = 0
for x in range(-300, 300):
    for y in range(-300, 300):
        #print(f'Trying {x},{y}')
        #example = State(x, y, 20, -10, 30, -5)
        #maxY = example.TryIt()
        real = State(x, y, 241, -97, 273, -63)
        maxY = real.TryIt()
        if maxY is not None:
            totalWinners += 1
            if (maxMaxY is None or maxY > maxMaxY):
                maxMaxY = maxY
print(maxMaxY)
print(totalWinners)
