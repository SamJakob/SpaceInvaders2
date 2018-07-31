import pygame
from entity.turret.controls.lib import xbox360_controller
from util.stage import Stage, TextPositions
from struct import GameState

class Menu:
    def __init__(self, application):
        # Store a reference to the application instance
        self.application = application

        # Import & load the play button
        self.playBtnImg = pygame.image.load("assets/sprites/ui/btn_play.png")

    def bind(self, screen):
        self.screen = screen

    def draw_frame(self):
        # Draw the title
        title = Stage.renderText(
            self.screen,
            self.application.titleFont,
            self.application.APPLICATION_NAME,
            TextPositions.CENTER_ALIGN,
            self.application.TEXT_COLOR
        )
        self.screen.blit(title.text, (title.pos_x, 200))

        # Draw the subtitle
        subtitle = Stage.renderText(
            self.screen,
            self.application.defaultFont,
            "Created by Sam Mearns",
            TextPositions.CENTER_ALIGN,
            self.application.TEXT_COLOR
        )
        self.screen.blit(subtitle.text, (subtitle.pos_x, 310))

        # Draw the play button
        playButtonRect = self.playBtnImg.get_rect()

        # Center the play button
        playButtonX = Stage.calculateCenterX(self.screen, playButtonRect)
        playButtonRect.x = playButtonX
        playButtonRect.y = 400

        # Change the play button on hover
        if playButtonRect.collidepoint(pygame.mouse.get_pos()):
            self.playButton = Stage.colorize(self.playBtnImg, (20, 20, 20), pygame.BLEND_RGBA_SUB)
        else:
            self.playButton = self.playBtnImg

        # Blit the play button
        self.screen.blit(self.playButton, playButtonRect)

        # Handle click event
        mouseDown = pygame.mouse.get_pressed()[0]
        if playButtonRect.collidepoint(pygame.mouse.get_pos()) and mouseDown:
            self.application.currentGameState = GameState.GAME_PLAY

        if pygame.joystick.get_count() > 0:
            controller = xbox360_controller.Controller(0)
            pressed = controller.get_buttons()

            if pressed[xbox360_controller.A] or pressed[xbox360_controller.X]:
                self.application.currentGameState = GameState.GAME_PLAY
