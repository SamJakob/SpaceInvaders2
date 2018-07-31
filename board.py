import pygame
from util.stage import Stage, TextPositions
from entity.enemy import EnemyType
from entity.enemy import Enemy
from entity.turret import Turret
from collections import namedtuple

from entity.turret.MovementControls import MovementControls
from entity.turret.controls.XboxControls import XboxControls

class Board:
    def __init__(self, application, screen):
        # Just store some references and instance variables
        self.screen = screen
        self.alternateCycle = False
        self.frameIndex = 0

        # Store a reference to the application instance
        self.application = application

        # Enemy layout
        self.enemies = self.build_enemy_wave([
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2],
            [3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3],
        ])

        # Turret(s)
        self.turrets = [
            Turret.Turret(XboxControls())
        ]

        # Set primary turret location
        self.turrets[0].x = Stage.calculateCenterX(
            self.screen,
            self.turrets[0].getRect()
        )
        self.turrets[0].y = self.screen.get_height() - self.turrets[0].getSize()[1]

    def bind(self, screen):
        self.screen = screen

    def draw_frame(self):
        # Draw Enemies:
        # Iterate over each row, and then each enemy in that row...
        for row in self.enemies:
            for enemy in row:
                # Scale the enemy sprite to the size defined in the object.
                enemySprite = pygame.transform.scale(
                    enemy.getSprite(self.alternateCycle),
                    enemy.getSize()
                )
                # Blit the enemy to the screen, in the co-ordinates defined
                # in the object.
                self.screen.blit(enemySprite, (enemy.getX(), enemy.getY()))

        # Move Turret:
        for turret in self.turrets:
            if turret.getMovementControls().moveLeft():
                turret.x -= 5
            if turret.getMovementControls().moveRight():
                turret.x += 5

        # Draw Turrets:
        for turret in self.turrets:
            self.screen.blit(turret.getSprite(), turret.getRect())

        # Final:
        # Alternate the sprites every 10 frames.
        # This slows down the alternating animation but gives you a lot
        # of control over the speed.
        self.frameIndex += 1
        if(self.frameIndex >= 10):
            self.alternateCycle = not self.alternateCycle
            self.frameIndex = 0

    def build_enemy_wave(self, wave_map):
        # Set the enemies to the wave map.
        enemies = wave_map
        # Now, iterate over the wave map and replace each type code
        # with an enemy of that type.
        rowNum = 1
        for row in enemies:
            colNum = 0
            for col in row:
                # Get the type ID of the enemy
                type = col
                # Instantiate an enemy and set its type
                col = Enemy.Enemy()
                # I don't make the type read-only, because for harder levels
                # it might be fun to make them switch type.
                col.setType(type)
                # and calculate the location and size of the enemy.
                meta = self.calculate_enemy_location_and_size(len(row), colNum, rowNum, 10)
                col.setSize(meta.size)
                col.setX(meta.x)
                col.setY(meta.y)

                enemies[rowNum - 1][colNum] = col

                colNum += 1
            rowNum += 1

        return enemies

    # row_enemy_count = The number of enemies in the row.
    # enemy_offset    = The enemy, or column, number.
    # row_offset      = The row number
    # row_gap         = The gap to leave between rows
    def calculate_enemy_location_and_size(self, row_enemy_count, enemy_offset, row_offset, row_gap):
        enemy_height = 32
        enemy_width = 32

        # enemy_gap = ((self.screen.get_width() - (enemy_width * row_enemy_count)) + 2) / row_enemy_count
        enemy_gap = 32
        outer_gap = (self.screen.get_width() - ((enemy_width + 32) * row_enemy_count)) / 2

        x = (enemy_offset * (enemy_gap + enemy_width)) + outer_gap
        y = (row_offset * (row_gap + enemy_height))

        EnemyLocationSize = namedtuple('EnemyLocationSize', ['x', 'y', 'size'])
        return EnemyLocationSize(x=x, y=y, size=(enemy_width, enemy_height))
