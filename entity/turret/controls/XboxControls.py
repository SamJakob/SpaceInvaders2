import pygame
from entity.turret.controls.lib import xbox360_controller
from entity.turret.controls.lib import xinput

class XboxControls():

    def __init__(self):
        if pygame.joystick.get_count() < 1:
            raise RuntimeError("Unable to locate Xbox 360 / Xbox One controller.")

        # Get xbox360_controller (pygame) controller instance
        self.controller = xbox360_controller.Controller(0)
        # Get xinput controller instance
        joysticks = xinput.XInputJoystick.enumerate_devices()
        if len(joysticks):
            self.xinput_joystick = joysticks[0]

    def moveLeft(self):
        if self.controller.get_left_stick()[0] <= -0.5:
            return True

    def moveRight(self):
        if self.controller.get_left_stick()[0] >= 0.5:
            return True

    def shoot(self):
        if self.controller.get_buttons()[xbox360_controller.A]:
            return True

    def feedback(self):
        pass
