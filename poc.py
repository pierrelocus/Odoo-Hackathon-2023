import pygame
import config

from game import Game

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Test game")

game = Game(screen)

screen.fill(config.BLACK)

while True:
    game.update()
    screen.fill(config.BLACK)
    pygame.display.flip()