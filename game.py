import pygame
import pytmx
import pyscroll

from player import Player
from dialogs import DialogBox
from map import Map
from map import MapManager

import json

alphabet = [
    pygame.K_a,
    pygame.K_b,
    pygame.K_c,
    pygame.K_d,
    pygame.K_e,
    pygame.K_f,
    pygame.K_g,
    pygame.K_h,
    pygame.K_i,
    pygame.K_j,
    pygame.K_k,
    pygame.K_l,
    pygame.K_m,
    pygame.K_n,
    pygame.K_o,
    pygame.K_p,
    pygame.K_q,
    pygame.K_r,
    pygame.K_s,
    pygame.K_t,
    pygame.K_u,
    pygame.K_v,
    pygame.K_w,
    pygame.K_x,
    pygame.K_y,
    pygame.K_z,
]

class Game:

    def __init__(self):
        # Démarrage
        self.running = True
        self.map = "world"
        self.last_move = False
        # Affichage de la fenêtre
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("BasiqueGame")
        self.player = Player(50,50)
        self.map_manager = MapManager(self.screen,self.player)
        # Définir le logo du jeu
        pygame.display.set_icon(self.player.get())




    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_ESCAPE]:
            self.running = False
        elif pressed[pygame.K_BACKSPACE]:
            self.current_user_input = self.current_user_input[:-1]
            print(self.current_user_input)
        elif pressed[pygame.K_UP]:
            self.player.move_player("up")
            self.last_move = 'UP'
        elif pressed[pygame.K_DOWN]:
            self.player.move_player("down")
            self.last_move = 'DOWN'
        elif pressed[pygame.K_RIGHT]:
            self.player.move_player("right")
            self.last_move = 'RIGHT'
        elif pressed[pygame.K_LEFT]:
            self.player.move_player("left")
            self.last_move = 'LEFT'

    def update(self):
        self.map_manager.update()

    def run(self):
        clock = pygame.time.Clock()

        # Clock
        while self.running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            clock.tick(60)

        pygame.quit()
