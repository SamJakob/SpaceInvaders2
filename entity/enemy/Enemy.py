import pygame
import random

from entity import Bullet

class Enemy:
    def __init__(self):
        # Define sprite variables
        self.speed_x = 40
        self.speed_y = 40

    def bindBoard(self, board):
        self.board = board

    def fireBullet(self):
        enemyBullet = Bullet.Bullet('enemy')
        enemyBullet.setX((self.x + (self.getSize()[0] / 2)) - enemyBullet.getSize()[0] / 2)
        enemyBullet.setY(self.y)
        self.board.bullets.append(enemyBullet)

    def setType(self, enemy_type):
        self.type = enemy_type

        # Define sprite paths
        self.spriteImage = "assets/sprites/enemy/enemy" + str(enemy_type) + "_0.png"
        self.spriteImageAlt = "assets/sprites/enemy/enemy" + str(enemy_type) + "_1.png"

        # Load sprites
        self.sprite = pygame.image.load(self.spriteImage)
        self.spriteAlt = pygame.image.load(self.spriteImageAlt)

    def getType(self):
        return self.type

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

    def getRect(self):
        return pygame.Rect(self.getLocation(), self.getSize())

    # Prompts the enemy class to consider firing a bullet.
    # This is run once per frame.
    def considerFireBullet(self):
        percentageChanceFiring = 0.15
        if random.random() < percentageChanceFiring / 100:
            self.fireBullet()
            return True
        return False
