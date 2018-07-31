import pygame

class Enemy:
    def __init__(self):
        # Define sprite variables
        self.speed_x = 40
        self.speed_y = 40

    def setType(self, enemy_type):
        # Define sprite paths
        self.spriteImage = "assets/sprites/enemy/enemy" + str(enemy_type) + "_0.png"
        self.spriteImageAlt = "assets/sprites/enemy/enemy" + str(enemy_type) + "_1.png"

        # Load sprites
        self.sprite = pygame.image.load(self.spriteImage)
        self.spriteAlt = pygame.image.load(self.spriteImageAlt)

    def getSprite(self, isAltSprite):
        if isAltSprite:
            return self.spriteAlt
        else:
            return self.sprite

    def setX(self, x):
        self.x = x

    def getX(self):
        return self.x

    def setY(self, y):
        self.y = y

    def getY(self):
        return self.y

    def setSize(self, size):
        self.size = size

    def getSize(self):
        return self.size

    def getLocation(self):
        return (self.x, self.y)
