import pygame

class Barrier:
    def __init__(self, board, x, y):
        self.board = board

        self.size = 8
        self.x = x
        self.y = y

        # The barrier shape template.
        # An 11 x 11 bitmap.
        self.barrier_shape = [
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
            [0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]

        # The barrier object structure.
        self.barrier_structure = []
        self.construct(self.barrier_shape)

    def setX(self, x):
        self.x = x

    def getX(self):
        return self.x

    def setY(self, y):
        self.y = y

    def getY(self):
        return self.y

    def construct(self, barrier_shape):
        size = self.size
        rowOffset = 0
        for row in self.barrier_shape:
            colOffset = 0
            for col in row:
                if col:
                    self.barrier_structure.append(Particle(colOffset + self.getX(), rowOffset + self.getY(), (size, size)))
                colOffset += size
            rowOffset += size


class Particle:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getSize(self):
        return self.size

    def setRect(self, rect):
        self.rect = rect

    def getRect(self):
        return self.rect
