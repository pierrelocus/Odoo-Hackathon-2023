import pygame
import config
from pygame.locals import *

class Player:
    def __init__(self, x_postition, y_position):
        print("player created")
        self.player = Rect(x_postition * config.SCALE, y_position * config.SCALE, config.SCALE, config.SCALE)

    def update(self):
        print("player updated")


    def update_position(self, x_change, y_change):
        if not (self.player.left == 0 and x_change < 0) and \
            not (self.player.left >= (config.WIDTH - config.SCALE) and x_change > 0):
            self.player.left += x_change * config.SCALE
        if not (self.player.top == 0 and y_change < 0) and \
            not (self.player.top >= (config.HEIGHT - config.SCALE) and y_change > 0):
            self.player.top += y_change * config.SCALE

    def render(self, screen):
        pygame.draw.rect(screen, config.WHITE, self.player, 4)

    # def is_obstacle_new_move(self, x_change, y_change):
        