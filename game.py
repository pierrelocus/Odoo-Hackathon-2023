import pygame
import pytmx
import pyscroll
import json

from player import Player
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

        # Charger la carte clasique
        tmx_data = pytmx.util_pygame.load_pygame("map.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3

        # Générer le joeur
        #player_position = tmx_data.get_object_by_name('player')
        self.player = Player(92, 296)

        # Définir le logo du jeu
        pygame.display.set_icon(self.player.get())

        # Les collisions
        self.walls = []
        self.panels = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == 'panel':
                self.panels.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner les différents calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)
        font = pygame.font.SysFont('Times New Roman', 50)
        texts = ['Hi', 'Hello', 'Who are ye?', 'Someone']
        self.text_renders = [font.render(text, True, (0, 0, 255)) for text in texts]
        self.space_released = True
        self.text_index = -1
        self.dialog_box = pygame.Rect(10, 10, 500, 200)
        self.letter_key_released = True
        self.is_on_prompt = False
        self.current_user_input = ""
        self.json_file = "data.json"
        self.enter_pressed = True

        # Porte de la maison


    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_ESCAPE]:
            self.running = False
        if any([pressed[letter] for letter in alphabet]) and self.letter_key_released:
            self.is_on_prompt = True
            self.letter_key_released = False
            for letter in alphabet:
                if pressed[letter]:
                    if pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]:
                        self.current_user_input += chr(letter - 32)
                    else:
                        self.current_user_input += chr(letter)
                    print(self.current_user_input)
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
        elif pressed[pygame.K_RETURN] and self.enter_pressed:
            listObj = []
            print("YA ZEBIH OMG")
            with open(self.json_file) as fjson:
                listObj = json.load(fjson)
                print(listObj)
            listObj.append({
                "story": self.current_user_input,
                "opening_date": "2023-12-12",
                "x_pos": 1,
                "y_pos": 443,
                "user": "Me",
                "themes": "IDK bro"
            })
            with open(self.json_file, 'w') as jsfile:
                json.dump(listObj, jsfile, indent=4, separators=(',',': '))
                print(listObj)

            self.current_user_input = ""
            self.is_on_prompt = True
            self.enter_pressed = False
        elif pressed[pygame.K_SPACE]:
            if self.is_on_prompt:
                self.current_user_input += chr(32)
            else:
                self.manage_action()
        if not pressed[pygame.K_SPACE] or not pressed[pygame.K_RETURN]:
            self.space_released = True
        if all([not pressed[letter] for letter in alphabet]):
            self.letter_key_released = True
        if not pressed[pygame.K_RETURN]:
            self.enter_pressed = True

    def manage_action(self):
        if self.space_released:
            for sprite in self.group.sprites():
                if sprite.feet.collidelist(self.panels) > -1:
                    print('In front of panel')
                    self.space_released = False
                    self.text_index = (self.text_index + 1) if (self.text_index + 1) != len(self.text_renders) else 0
        if self.text_index != -1:
            self.screen.blit(self.text_renders[self.text_index], (0, 0), self.dialog_box)


    def update(self):
        self.group.update()
        # Vérification des collisions
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self):
        clock = pygame.time.Clock()

        # Clock
        while self.running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            clock.tick(60)

        pygame.quit()
