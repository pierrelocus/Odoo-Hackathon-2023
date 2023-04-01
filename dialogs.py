import pygame


class DialogBox:

    def __init__(self, panel=False, texts=[], years=False, player=False):
        if texts:
            self.texts = texts
        if not panel:
            self.box = pygame.image.load('./dialog/dialogs_box.png')
            self.box = pygame.transform.scale(self.box, (800, 80))
            self.x_position = 560
            self.y_position = 800
            self.x_text_position = 650
            self.y_text_position = 825
            self.font = pygame.font.Font('./dialog/dialog_font.ttf',26)
            self.color = (0, 0, 0)
        else:
            if panel == 'new':
                self.box = pygame.image.load('./dialog/wooden_panel_retro_add_new.png')
            else:
                self.box = pygame.image.load('./dialog/wooden_panel_retro.png')
            self.box = pygame.transform.scale(self.box, (1680, 800))
            self.x_position = 120
            self.y_position = 120
            self.x_text_position = 320
            self.y_text_position = 320
            self.font = pygame.font.Font('./dialog/dialog_font.ttf',28)
            self.color = (0, 0, 0)
        self.panel = panel
        self.text_index = 0
        self.reading = True
        self.years_to_open = years or 0

    def render(self,screen):
        if self.reading:
            screen.blit(self.box, (self.x_position, self.y_position))
            if len(self.texts):
                self.blit_text(screen, self.texts[self.text_index], (self.x_text_position, self.y_text_position), self.font)
            if self.panel == 'new':
                years = self.font.render('Closed for : %s Years' % self.years_to_open, False, pygame.Color('white'))
                screen.blit(years, (1300, 170))

    def blit_text(self, surface, text, pos, font, color=pygame.Color('white')):
        color = self.color
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width - 250:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.

    def next_text(self):
        self.text_index += 1
        if self.text_index >= len(self.texts):
            self.reading = False
            self.text_index = 0
