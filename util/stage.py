import pygame
from enum import Enum
from collections import namedtuple

class Stage:
    def distributeX(screen, count, space, size):
        xOffset = ((screen.get_width() - (space * count) - (size * count)) / 2) + (space / 2)
        xValues = []
        for i in range(0, count):
            xValues.append(xOffset)
            xOffset += size + space
        return xValues

    def calculateRightX(screen, rectangle):
        return (screen.get_width() - rectangle.width) - 20

    def calculateCenterX(screen, rectangle):
        return (screen.get_width() / 2) - (rectangle.width / 2)

    def renderText(screen, font, text, position_x, color = (255, 255, 255)):
        renderedText = font.render(
            text,         # Text to render
            True,         # Should antialias text
            color         # The font color
        )

        if position_x == TextPositions.LEFT_ALIGN:
            titleX = 20
        elif position_x == TextPositions.CENTER_ALIGN:
            titleX = Stage.calculateCenterX(screen, renderedText.get_rect())
        elif position_x == TextPositions.RIGHT_ALIGN:
            titleX = Stage.calculateRightX(screen, renderedText.get_rect())

        TextRender = namedtuple('TextRender', ['text', 'pos_x'])
        return TextRender(text=renderedText, pos_x=titleX)

    def colorize(image, newColor, alg):
        """
        Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
        original).
        :param image: Surface to create a colorized copy of
        :param newColor: RGB color to use (original alpha values are preserved)
        :return: New colorized Surface instance
        """
        image = image.copy()

        # zero out RGB values
        # image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        # add in new RGB values
        image.fill(newColor[0:3] + (0,), None, alg)

        return image

class TextPositions(Enum):
    LEFT_ALIGN = 0
    CENTER_ALIGN = 1
    RIGHT_ALIGN = 2
