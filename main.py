# Import dependencies
import sys
import pygame
from pygame import locals as pygl
# Import application classes & utils
from app_struct import GameState
from board import Board
from menu import Menu
from util.stage import Stage, TextPositions


# PARAM: Whether or not the application should display in fullscreen
APPLICATION_FULLSCRN = True
APPLICATION_NAME = "Space Invaders 2"
APPLICATION_PRIMARY_CONTROLS = "Xbox"  # Xbox / Keyboard

FOREGROUND_COLOR = (52, 255, 0)
TEXT_COLOR = (255, 255, 255)
BULLET_COLOR = (255, 52, 0)
ENEMY_BULLET_COLOR = (255, 255, 255)

# Define application class
class Application:
    def __init__(self):
        # Set application-wide constants
        self.APPLICATION_NAME = APPLICATION_NAME
        self.APPLICATION_PRIMARY_CONTROLS = APPLICATION_PRIMARY_CONTROLS
        self.FOREGROUND_COLOR = FOREGROUND_COLOR
        self.TEXT_COLOR = TEXT_COLOR
        self.BULLET_COLOR = BULLET_COLOR
        self.ENEMY_BULLET_COLOR = ENEMY_BULLET_COLOR

        # Set initial application state variables
        self.score = 0
        self.lives = 3

        # Init required pygame modules
        pygame.font.init()
        pygame.joystick.init()

        # Calculate pygame dimensions
        displayDimensions = (800, 600)
        displayParameters = 0
        if APPLICATION_FULLSCRN:
            displayParameters = pygame.FULLSCREEN

        # Set up pygame and its modules
        self.defaultFont = pygame.font.Font("assets/fonts/space_invaders.ttf", 15)
        self.titleFont = pygame.font.Font("assets/fonts/space_invaders.ttf", 70)
        self.screen = pygame.display.set_mode(displayDimensions, displayParameters)
        pygame.display.set_caption(APPLICATION_NAME)

        # Setup the menu
        self.menu = Menu(self)
        self.menu.bind(self.screen)

        # Setup the board
        self.board = Board(self, self.screen)
        self.board.bind(self.screen)

        # Set the current state to the game menu
        self.currentGameState = GameState.GAME_MENU

    def run(self):
        # Execute game loop
        while self.currentGameState != GameState.GAME_EXIT:
            for event in pygame.event.get():
                # Exit the game when the window is closed
                if event.type == pygame.QUIT:
                    sys.exit()

                # Alt+F4 is not handled by default; we'll make it close the
                # game immediately. (Alt+F4, traditionally means terminate.)
                pressedKeys = pygame.key.get_pressed()
                if pressedKeys[pygl.K_LALT] and pressedKeys[pygl.K_F4]:
                    sys.exit()

            # Get current tick time
            initialTime = pygame.time.get_ticks()

            # The game menu loop
            if self.currentGameState == GameState.GAME_MENU:
                # Blank the screen
                self.screen.fill((0, 0, 0))

                # Update the menu.
                # This handles most of the heavy lifting.
                self.menu.draw_frame()

            # The game play loop
            if self.currentGameState == GameState.GAME_PLAY:
                # Blank the screen
                self.screen.fill((0, 0, 0))

                # Update the board.
                # This handles most of the heavy lifting.
                self.board.draw_frame()

            if self.currentGameState == GameState.GAME_END:
                gameOverText = Stage.renderText(
                    self.screen,
                    self.titleFont,
                    "Game Over",
                    TextPositions.CENTER_ALIGN,
                    self.FOREGROUND_COLOR
                )

                gotr = gameOverText.text.get_rect()
                backgroundRect = pygame.Rect(
                    gameOverText.pos_x - 20,
                    (self.screen.get_height() / 2) - (gameOverText.text.get_rect().height / 2) - 20,
                    gotr.width + 40,
                    gotr.height + 40
                )
                pygame.draw.rect(self.screen, (0, 0, 0), backgroundRect)

                self.screen.blit(gameOverText.text, (
                    gameOverText.pos_x,
                    (self.screen.get_height() / 2) - (gameOverText.text.get_rect().height / 2)
                ))

            # Render frame
            pygame.display.flip()

            # Delay for remainder of processing time
            finalTime = pygame.time.get_ticks()
            pygame.time.wait(40 - (initialTime - finalTime))

if __name__ == "__main__":
    # Start running application
    Application().run()
