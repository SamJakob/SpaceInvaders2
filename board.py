import pygame
from app_struct import delay, GameState
from util.stage import Stage, TextPositions
from entity.enemy import EnemyType
from entity.enemy import Enemy
from entity.turret import Turret
from entity import Bullet
from entity import Barrier
from collections import namedtuple

from entity.turret.MovementControls import MovementControls
from entity.turret.controls.XboxControls import XboxControls
from entity.turret.controls.KeyboardControls import KeyboardControls

class Board:
    def __init__(self, application, screen):
        # Just store some references and instance variables
        self.screen = screen
        self.alternateCycle = False
        self.frameIndex = 0
        self.enemyDirection = False
        self.playerReloaded = True

        # Some 'constants'
        self.rowGap = 10

        # Store a reference to the application instance
        self.application = application

        # Enemy layout
        self.enemies = self.build_enemy_wave([
            [3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3],
            [2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2],
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
        ])

        # Turret(s)
        self.turrets = [
            Turret.Turret(eval(self.application.APPLICATION_PRIMARY_CONTROLS + "Controls()"))
        ]

        # Bullets
        self.bullets = []

        # Barriers
        tempBarrier = Barrier.Barrier(self, 0, 0)
        barrierSize = len(tempBarrier.barrier_shape[0]) * tempBarrier.size
        xValues = Stage.distributeX(self.screen, 4, 64, barrierSize)
        self.barriers = [
            Barrier.Barrier(self, xValues[0], screen.get_height() - (self.turrets[0].getSize()[1] + 175)),
            Barrier.Barrier(self, xValues[1], screen.get_height() - (self.turrets[0].getSize()[1] + 175)),
            Barrier.Barrier(self, xValues[2], screen.get_height() - (self.turrets[0].getSize()[1] + 175)),
            Barrier.Barrier(self, xValues[3], screen.get_height() - (self.turrets[0].getSize()[1] + 175))
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

        # Move Enemies:
        if self.frameIndex == 19 and self.alternateCycle:
            # Leftermost Enemy
            leftermostEnemy = None
            leftermostEnemyX = self.screen.get_width()

            # Rightermost Enemy
            rightermostEnemy = None  # Enemy
            rightermostEnemyX = 0

            for row in self.enemies:
                for enemy in row:
                    enemy.setX(enemy.getX() + 32 * (-1 if self.enemyDirection else 1))
                    if enemy.getX() > rightermostEnemyX:
                        rightermostEnemy = enemy
                        rightermostEnemyX = enemy.getX()
                    if enemy.getX() < leftermostEnemyX:
                        leftermostEnemy = enemy
                        leftermostEnemyX = enemy.getX()
            if rightermostEnemyX > self.screen.get_width() - 65:
                for row in self.enemies:
                    for enemy in row:
                        enemy.setY(enemy.getY() + enemy.getSize()[1] + self.rowGap)
                self.enemyDirection = not self.enemyDirection
            if leftermostEnemyX < 64:
                for row in self.enemies:
                    for enemy in row:
                        enemy.setY(enemy.getY() + enemy.getSize()[1] + self.rowGap)
                self.enemyDirection = not self.enemyDirection

        # Draw Barrier Blocks
        for barrier in self.barriers:
            for particle in barrier.barrier_structure:
                particleRect = pygame.Rect(
                    (particle.getX(), particle.getY()),
                    particle.getSize()
                )
                pygame.draw.rect(
                    self.screen,
                    self.application.FOREGROUND_COLOR,
                    particleRect
                )
                particle.setRect(particleRect)

        # Prompt Enemy Handlers
        for row in self.enemies:
            for enemy in row:
                if enemy.considerFireBullet():
                    for turret in self.turrets:
                        turret.addScore(5)

        # Display HUD
        lives = self.turrets[0].getLives()
        livesText = Stage.renderText(
            self.screen,
            self.application.defaultFont,
            "Lives: " + str(lives),
            TextPositions.LEFT_ALIGN,
            self.application.TEXT_COLOR
        )
        self.screen.blit(livesText.text, (livesText.pos_x, 20))

        siText = Stage.renderText(
            self.screen,
            self.application.defaultFont,
            self.application.APPLICATION_NAME,
            TextPositions.CENTER_ALIGN,
            self.application.TEXT_COLOR
        )
        self.screen.blit(siText.text, (siText.pos_x, 20))

        score = self.turrets[0].getScore()
        scoreText = Stage.renderText(
            self.screen,
            self.application.defaultFont,
            "Score: " + str(score),
            TextPositions.RIGHT_ALIGN,
            self.application.TEXT_COLOR
        )
        self.screen.blit(scoreText.text, (scoreText.pos_x, 20))

        # Move Turret:
        for turret in self.turrets:
            if turret.getMovementControls().moveLeft():
                if turret.x > 0:
                    turret.x -= 5
            if turret.getMovementControls().moveRight():
                if turret.x < self.screen.get_width() - turret.getSize()[0]:
                    turret.x += 5
            if turret.getMovementControls().shoot():
                if self.playerReloaded:
                    playerBullet = Bullet.Bullet('player')
                    playerBullet.setX((turret.x + (turret.getSize()[0] / 2)) - playerBullet.getSize()[0] / 2)
                    playerBullet.setY(turret.y)
                    self.bullets.append(playerBullet)
                    self.playerReloaded = False

                    @delay(0.5)
                    def reloadPlayerTurret(self):
                        self.playerReloaded = True

                    reloadPlayerTurret(self)

        # Draw Turrets:
        for turret in self.turrets:
            self.screen.blit(turret.getSprite(), turret.getRect())

        # Move Bullets:
        for bullet in self.bullets:
            if bullet.getOwner() == 'player':
                bullet.setY(bullet.getY() + -bullet.speed)
            else:
                bullet.setY(bullet.getY() + bullet.speed)

        # Draw Bullets:
        for bullet in self.bullets:
            bulletColor = self.application.ENEMY_BULLET_COLOR
            if bullet.getOwner() == 'player':
                bulletColor = self.application.BULLET_COLOR
            pygame.draw.rect(
                self.screen,
                bulletColor,
                bullet.getRect()
            )

        # Bullet Hit Detection
        for bullet in self.bullets:
            for barrier in self.barriers:
                for particle in barrier.barrier_structure:
                    if bullet.getRect().colliderect(particle.getRect()):
                        barrier.barrier_structure.remove(particle)
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
                        if bullet.getOwner() == 'player':
                            for turret in self.turrets:
                                turret.addScore(10)
                        elif bullet.getOwner() == 'enemy':
                            for turret in self.turrets:
                                turret.removeScore(10)

            if bullet.getOwner() == 'player':
                for row in self.enemies:
                    for enemy in row:
                        if bullet.getRect().colliderect(enemy.getRect()):
                            for turret in self.turrets:
                                turret.addScore(enemy.getType() * 100)
                            row.remove(enemy)
                            self.bullets.remove(bullet)

            elif bullet.getOwner() == 'enemy':
                for turret in self.turrets:
                    if bullet.getRect().colliderect(turret.getRect()):
                        self.bullets.remove(bullet)

                        if turret.getLives() <= 1:
                            self.application.currentGameState = GameState.GAME_END

                        turret.setLives(turret.getLives() - 1)
                        turret.x = Stage.calculateCenterX(
                            self.screen,
                            turret.getRect()
                        )

        # Final:
        # Alternate the sprites every 10 frames.
        # This slows down the alternating animation but gives you a lot
        # of control over the speed.
        self.frameIndex += 1
        if(self.frameIndex >= 20):
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
                col.bindBoard(self)
                # I don't make the type read-only, because for harder levels
                # it might be fun to make them switch type.
                col.setType(type)
                # and calculate the location and size of the enemy.
                meta = self.calculate_enemy_location_and_size(len(row), colNum, rowNum, self.rowGap)
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
