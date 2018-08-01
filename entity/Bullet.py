import pygame

class Bullet:
    def __init__(self, owner = 'unknown'):
        self.owner = owner
        self.speed = 10

        self.width = 5
        self.height = 10

        self.size = (self.width, self.height)

    def setSpeed(self, speed):
        self.speed = speed

    def getOwner(self):
        return self.owner

    def setX(self, x):
        self.x = x

    def getX(self):
        return self.x

    def setY(self, y):
        self.y = y

    def getY(self):
        return self.y

    def getSize(self):
        return self.size

    def getLocation(self):
        return (self.x, self.y)

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
