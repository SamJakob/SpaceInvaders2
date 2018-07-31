import pygame

class Turret:
    def __init__(self, MovementControls):
        self.speed = 20

        self.spriteImage = "assets/sprites/turret/shooter.png"
        self.sprite = pygame.image.load(self.spriteImage)

        spriteRect = self.sprite.get_rect()
        self.size = (spriteRect.width, spriteRect.height)

        self.x = 0
        self.y = 0

        self.movementControls = MovementControls

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
