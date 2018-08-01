import pygame

class Turret:
    def __init__(self, MovementControls):
        self.speed = 40
        self.lives = 3
        self.score = 0

        self.spriteImage = "assets/sprites/turret/shooter.png"
        self.sprite = pygame.image.load(self.spriteImage)

        spriteRect = self.sprite.get_rect()
        self.size = (spriteRect.width, spriteRect.height)

        self.x = 0
        self.y = 0

        self.movementControls = MovementControls

    def getScore(self):
        return self.score

    def setScore(self, score):
        self.score = score

    def addScore(self, scoreDelta):
        self.score += scoreDelta

    def removeScore(self, negativeScoreDelta):
        self.score -= negativeScoreDelta

    def getLives(self):
        return self.lives

    def setLives(self, lives):
        self.lives = lives

    def getSprite(self):
        return self.sprite

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
        return pygame.Rect(
            self.x,
            self.y,
            self.getSize()[0],
            self.getSize()[1]
        )

    def setMovementControls(self, MovementControls):
        self.movementControls = MovementControls

    def getMovementControls(self):
        return self.movementControls
