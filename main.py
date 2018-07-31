# Import dependencies
import sys
import pygame
from pygame import locals as pygl
# Import application classes & utils
from struct import GameState
from board import Board
from menu import Menu


# PARAM: Whether or not the application should display in fullscreen
APPLICATION_FULLSCRN = False
APPLICATION_NAME = "Space Invaders 2"

FOREGROUND_COLOR = (52, 255, 0)
TEXT_COLOR = (255, 255, 255)


# Define application class
class Application:
    def __init__(self):
        # Set application-wide constants
        self.APPLICATION_NAME = APPLICATION_NAME
        self.FOREGROUND_COLOR = FOREGROUND_COLOR
        self.TEXT_COLOR = TEXT_COLOR

        # Set initial application state variables
        self.score = 0
        self.lives = 3

        # Init required pygame modules
        pygame.font.init()
        pygame.joystick.init()

        # Set up pygame and its modules
        self.defaultFont = pygame.font.Font("assets/fonts/space_invaders.ttf", 15)
        self.titleFont = pygame.font.Font("assets/fonts/space_invaders.ttf", 70)
        self.screen = pygame.display.set_mode((800, 600), APPLICATION_FULLSCRN)
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

            # Blank the screen
            self.screen.fill((0, 0, 0))

            # The game menu loop
            if self.currentGameState == GameState.GAME_MENU:
                # Update the menu.
                # This handles most of the heavy lifting.
                self.menu.draw_frame()

            # The game play loop
            if self.currentGameState == GameState.GAME_PLAY:
                # Update the board.
                # This handles most of the heavy lifting.
                self.board.draw_frame()

            # Render frame
            pygame.display.flip()

            # Delay for remainder of processing time
            finalTime = pygame.time.get_ticks()
            pygame.time.wait(40 - (initialTime - finalTime))

if __name__ == "__main__":
    # Start running application
    Application().run()
