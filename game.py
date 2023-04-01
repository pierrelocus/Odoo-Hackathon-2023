import pygame
import pytmx
import pyscroll

from player import Player, PlayerStatus
from dialogs import DialogBox

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

        # Charger la carte clasique
        self.tmx_data = pytmx.util_pygame.load_pygame("map.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 3

        # Générer le joeur
        player_position = self.tmx_data.get_object_by_name('player')
        self.player = Player(player_position.x,player_position.y)
        self.dialog_box = DialogBox()

        # Définir le logo du jeu
        pygame.display.set_icon(self.player.get())

        # Les collisions
        self.walls = []
        self.hints = []
        self.panels = []
        
        for obj in self.tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "hint":
                self.hints.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == 'panel':
                self.panels.append({'name': obj.name, 'rect': pygame.Rect(obj.x, obj.y, obj.width, obj.height)})

        # Dessiner les différents calques
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player)

        # Dessiner les différents calques
        font = pygame.font.SysFont('Times New Roman', 50)
        texts = ['Hi', 'Hello', 'Who are ye?', 'Someone']
        self.text_renders = [font.render(text, True, (0, 0, 255)) for text in texts]
        self.space_released = True
        self.text_index = -1
        self.letter_key_released = True
        self.is_on_prompt = False
        self.is_display_wooden_panel = False
        self.current_user_input = ""
        self.json_file = "data.json"
        self.enter_pressed = True

        file_data = open('data.json')
        self.all_text_data = json.load(file_data)
        self.panel_texts = {}
        for row in self.all_text_data:
            if 'type' in row and row['type'] == 'panel':
                self.panel_texts[row['panel_id']] = row['story']
        print(self.panel_texts)
        file_data.close()
        self.current_years_to_open_new_panel = 5

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
        elif pressed[pygame.K_RETURN] and self.enter_pressed and self.current_user_input:
            listObj = []
            print("YA ZEBIH OMG")
            with open(self.json_file) as fjson:
                listObj = json.load(fjson)
            
            for obj in listObj:
                print(obj)
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

            self.current_user_input = ""
            self.is_on_prompt = True
            self.enter_pressed = False
        elif pressed[pygame.K_SPACE]:
            if self.is_on_prompt:
                self.current_user_input += chr(32)
        if not pressed[pygame.K_SPACE]:
            self.space_released = True
        if all([not pressed[letter] for letter in alphabet]):
            self.letter_key_released = True
        if not pressed[pygame.K_RETURN]:
            self.enter_pressed = True

    def update(self):
        self.group.update()
        # Vérification des collisions
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def show_dialog_box(self, string, wooden_panel_type=False):
        self.dialog_box = DialogBox(panel=wooden_panel_type, texts=[string], years=self.current_years_to_open_new_panel)
        self.dialog_box.render(self.screen)

    def run(self):
        clock = pygame.time.Clock()

        # Clock
        while self.running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            self.show_dialog = False
            for sprite in self.group.sprites():
                if sprite.feet.collidelist([panel['rect'] for panel in self.panels]) > -1:
                    self.is_on_prompt = True
                    for panel in self.panels:
                        if sprite.feet.collidelist([panel['rect']]) > -1 and not ('new' in panel['name']):
                            self.show_dialog_box('Oh here is the panel of \{firstname\}')
                            self.show_dialog = True
                            break
                if self.show_dialog:
                    break
            if self.is_display_wooden_panel:
                self.player.status = PlayerStatus.LOCK
                for sprite in self.group.sprites():
                    for panel in self.panels:
                        if sprite.feet.collidelist([panel['rect']]) > -1:
                            if not 'new' in panel['name']:
                                self.show_dialog_box(self.panel_texts[panel['name']], wooden_panel_type='read')
                            else:
                                self.show_dialog_box(self.current_user_input, wooden_panel_type='new')
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.player.status = PlayerStatus.FREE
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    print('GOT KEY DOWN')
                    if event.key == pygame.K_RETURN:
                        print('display wooden panel : %s , is on prompt : %s' % (self.is_display_wooden_panel, self.is_on_prompt))
                        if self.is_display_wooden_panel:
                            self.is_display_wooden_panel = False
                            self.player.status = PlayerStatus.FREE
                            self.is_on_prompt = False
                        if self.is_on_prompt:
                            self.current_user_input = ""
                            self.is_display_wooden_panel = True
                        print('22 display wooden panel : %s , is on prompt : %s' % (self.is_display_wooden_panel, self.is_on_prompt))
                    print('Wooden panel ? %s' % self.is_display_wooden_panel)
                    if event.key == pygame.K_KP_PLUS:
                        if self.is_display_wooden_panel:
                            self.current_years_to_open_new_panel += 5
                    if event.key == pygame.K_KP_MINUS:
                        if self.is_display_wooden_panel:
                            self.current_years_to_open_new_panel -= 5

                    if event.unicode == "?":
                        self.current_user_input += "?"
                    elif event.unicode == "!":
                        self.current_user_input += "!"
                    elif event.unicode == ",":
                        self.current_user_input += ","
                    elif event.unicode == ".":
                        self.current_user_input += "."
                    elif event.unicode == "'":
                        self.current_user_input += "'"

            clock.tick(60)

        pygame.quit()
