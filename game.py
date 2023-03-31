import pygame
import config
from player import Player
from game_state import GameState

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.objects = []
        self.game_state = GameState.NONE

    def set_up(self):
        player = Player(1, 1)
        self.player = player
        self.objects.append(player)
        self.game_state = GameState.RUNNING

    def update(self):
        self.screen.fill(config.BLACK)
        self.handle_events()

        for object in self.objects:
            object.render(self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = GameState.ENDED
            #     handle key events
        keys = pygame.key.get_pressed()
        print(keys)
        if keys[pygame.K_ESCAPE]:
            self.game_state = GameState.ENDED
        if keys[pygame.K_w]: # up
            self.player.update_position(0, -1)
        if keys[pygame.K_s]: # down
            self.player.update_position(0, 1)
        if keys[pygame.K_a]: # up
            self.player.update_position(-1, 0)
        if keys[pygame.K_d]: # up
            self.player.update_position(1, 0)
