import pygame
import config

class Player:
    def __init__(self, x_postition, y_position):
        print("player created")
        self.position = [x_postition, y_position]

    def update(self):
        print("player updated")

    def update_position(self, x_change, y_change):
        print('Positions : %s %s' % (self.position[0], self.position[1]))
        if not (self.position[0] == 0 and x_change < 0) and \
            not (self.position[0] * config.SCALE >= 590 and x_change > 0):
            self.position[0] += x_change
        if not (self.position[1] == 0 and y_change < 0) and \
            not (self.position[1] * config.SCALE >= 390 and y_change > 0):
            self.position[1] += y_change

    def render(self, screen):
        pygame.draw.rect(screen, config.WHITE, (self.position[0] * config.SCALE, self.position[1] * config.SCALE, config.SCALE, config.SCALE), 4)
