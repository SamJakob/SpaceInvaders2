import pygame

class KeyboardControls():

    def __init__(self):
        pass

    def moveLeft(self):
        if pygame.key.get_pressed()[pygame.locals.K_LEFT]:
            return True

    def moveRight(self):
        if pygame.key.get_pressed()[pygame.locals.K_RIGHT]:
            return True

    def shoot(self):
        if pygame.key.get_pressed()[pygame.locals.K_SPACE]:
            return True

    def feedback(self):
        pass
