import pygame
import pygame.mixer
import pytmx
import pyscroll
import datetime
from dateutil.relativedelta import relativedelta
import uuid

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
        pygame.mixer.music.load("Shire_oasis.mp3")
        # Affichage de la fenêtre
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("BasiqueGame")
        self.player = Player(50,50)
        self.dialog_box = False
        # Définir le logo du jeu
        pygame.display.set_icon(self.player.get())
        self.tmx_data = pytmx.util_pygame.load_pygame("map.tmx")
        self.panels = []
        for obj in self.tmx_data.objects:
            if obj.type == 'panel':
                self.panels.append({'name': obj.name, 'rect': pygame.Rect(obj.x, obj.y, obj.width, obj.height)})
        
        self.space_released = True
        self.is_on_prompt = False
        self.is_display_wooden_panel = False
        self.current_user_input = ""
        self.json_file = "data.json"
        self.enter_pressed = True
        self.a_pressed = True
        self.b_pressed = True
        self.c_pressed = True
        self.d_pressed = True
        self.e_pressed = True
        self.f_pressed = True
        self.g_pressed = True   
        self.h_pressed = True
        self.i_pressed = True
        self.j_pressed = True
        self.k_pressed = True
        self.l_pressed = True
        self.m_pressed = True
        self.n_pressed = True
        self.o_pressed = True
        self.p_pressed = True
        self.q_pressed = True
        self.r_pressed = True
        self.s_pressed = True
        self.t_pressed = True
        self.u_pressed = True
        self.v_pressed = True
        self.w_pressed = True
        self.x_pressed = True
        self.y_pressed = True
        self.z_pressed = True
        self.show_dialog = False

        file_data = open('data.json')
        self.all_text_data = json.load(file_data)
        self.panel_texts = {}
        self.game_panels = {}
        self.current_session_game_panels = {}

        for row in self.all_text_data:
            if 'type' in row and row['type'] == 'game_panel':
                self.game_panels[row['panel_id']] = (row['x_pos'], row['y_pos'])
                self.panels.append({'name': row['panel_id'], 'rect': pygame.Rect(row['x_pos'], row['y_pos'], 28, 33)})
            if 'type' in row and row['type'] == 'panel':
                if 'opening_date' in row and row['opening_date'] > datetime.date.today().strftime('%Y-%m-%d'):
                    self.panel_texts[row['panel_id']] = 'Open on %s' % row['opening_date']
                else:
                    self.panel_texts[row['panel_id']] = row['story']
    
        file_data.close()
        self.current_years_to_open_new_panel = 5
        self.current_panel_writing = False
        self.backspace_released = True
        self.is_menu_open = False
        self.menu_position_x = 0
        self.menu_position_y = 0

        self.map_manager = MapManager(self.screen,self.player, panels=self.game_panels)

    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if any([pressed[letter] for letter in alphabet]):
            self.is_on_prompt = True
            for letter in alphabet:
                if pressed[letter] and getattr(self, chr(letter) + '_pressed'):
                    setattr(self, chr(letter) + '_pressed', False)
                    if pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]:
                        self.current_user_input += chr(letter - 32)
                    else:
                        self.current_user_input += chr(letter)
                
        elif pressed[pygame.K_BACKSPACE] and self.backspace_released:
            self.backspace_released = False
            self.current_user_input = self.current_user_input[:-1]
        
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
            with open(self.json_file) as fjson:
                listObj = json.load(fjson)
            if self.current_user_input:
                listObj.append({
                    "story": self.current_user_input,
                    "opening_date": (datetime.date.today() + relativedelta(years=self.current_years_to_open_new_panel)).strftime('%Y-%m-%d'),
                    "x_pos": 1,
                    "y_pos": 443,
                    "user": "Me",
                    'panel_id': self.current_panel_writing['name'],
                    "themes": "",
                    "type": "panel",
                })
            with open(self.json_file, 'w') as jsfile:
                json.dump(listObj, jsfile, indent=4, separators=(',',': '))
            file_data = open('data.json')
            self.all_text_data = json.load(file_data)
            self.panel_texts = {}
            self.game_panels = {}
            for row in self.all_text_data:
                if 'type' in row and row['type'] == 'game_panel':
                    self.game_panels[row['panel_id']] = (row['x_pos'], row['y_pos'])
                    self.panels.append({'name': row['panel_id'], 'rect': pygame.Rect(row['x_pos'], row['y_pos'], 28, 33)})
                if 'type' in row and row['type'] == 'panel':
                    if 'opening_date' in row and row['opening_date'] > datetime.date.today().strftime('%Y-%m-%d'):
                        self.panel_texts[row['panel_id']] = 'Open on %s' % row['opening_date']
                    else:
                        self.panel_texts[row['panel_id']] = row['story']
            file_data.close()
            self.current_user_input = ""
            self.is_on_prompt = True
            self.enter_pressed = False
        if pressed[pygame.K_SPACE]:
            if self.is_on_prompt and self.space_released:
                self.space_released = False
                self.current_user_input += chr(32)
        if not pressed[pygame.K_SPACE]:
            self.space_released = True
        if not pressed[pygame.K_RETURN]:
            self.enter_pressed = True
        if not pressed[pygame.K_BACKSPACE]:
            self.backspace_released = True
        for letter in alphabet:
            if not pressed[letter]:
                setattr(self, chr(letter) + '_pressed', True)
        if pressed[pygame.K_ESCAPE]:
            self.running = False

    def update(self):
        self.map_manager.update()

    def show_dialog_box(self, string, wooden_panel_type=False):
        self.dialog_box = DialogBox(panel=wooden_panel_type, texts=[string], years=self.current_years_to_open_new_panel, player=self.player)
        self.dialog_box.render(self.screen)

    def run(self):
        pygame.mixer.music.play()
        clock = pygame.time.Clock()

        # import moviepy.editor as meditor
        # clip = meditor.VideoFileClip('POKEMON_START.mp4')
        # clip.preview()

        while self.running:

            self.player.save_location()
            self.handle_input()
            self.update()
            self.map_manager.draw()
            for sprite in self.map_manager.get_group().sprites():
                if sprite.feet.collidelist([panel['rect'] for panel in self.map_manager.get_panels()]) > -1:
                    self.is_on_prompt = True
                    for panel in self.map_manager.get_panels():
                        if sprite.feet.collidelist([panel['rect']]) > -1:
                            if not 'new' in panel['name'] or ('new' in panel['name'] and panel['name'] in self.panel_texts.keys()):
                                self.show_dialog_box('Oh ! Someone let a message here.')
                            else:
                                self.show_dialog_box('An empty panel, I could write something.')
                            self.show_dialog = True
                            break
                if self.show_dialog:
                    break
            if self.is_display_wooden_panel:
                for sprite in self.map_manager.get_group().sprites():
                    for panel in self.map_manager.get_panels():
                        if sprite.feet.collidelist([panel['rect']]) > -1:
                            self.current_panel_writing = panel
                            if not 'new' in panel['name'] or ('new' in panel['name'] and panel['name'] in self.panel_texts.keys()):
                                self.show_dialog_box(self.panel_texts[panel['name']], wooden_panel_type='read')
                            else:
                                self.show_dialog_box(self.current_user_input, wooden_panel_type='new')

            # If we try to show dialog after the flip, we are after the update each time
            if self.is_menu_open:
                pos = (self.menu_position_x, self.menu_position_y)
                self.dialogBox = DialogBox(menu=True, mouse_coord=pos, screen=self.screen, real_mouse_coord=pygame.mouse.get_pos())

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    print(self.player.position[0])
                    print(self.player.position[1])
                    if event.key == pygame.K_RETURN:
                    
                        if self.is_display_wooden_panel:
                            self.is_display_wooden_panel = False
                            self.is_on_prompt = False
                        if self.is_on_prompt:
                            self.current_years_to_open_new_panel = 5
                            self.current_user_input = ""
                            self.is_display_wooden_panel = True
                    
                
                    if event.key == pygame.K_KP_PLUS:
                        if self.is_display_wooden_panel:
                            self.current_years_to_open_new_panel += 1
                    if event.key == pygame.K_KP_MINUS:
                        if self.is_display_wooden_panel:
                            if self.current_years_to_open_new_panel > 1:
                                self.current_years_to_open_new_panel -= 1

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
