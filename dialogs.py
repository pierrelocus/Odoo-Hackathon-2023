import pygame


class DialogBox:

    def __init__(self, panel=False, texts=[], years=False):
        if texts:
            self.texts = texts
        if not panel:
            self.box = pygame.image.load('./dialog/dialogs_box.png')
            self.box = pygame.transform.scale(self.box, (550, 50))
            self.x_position = 600
            self.y_position = 600
            self.font = pygame.font.Font('./dialog/dialog_font.ttf',18)
            self.color = (0, 0, 0)
        else:
            if panel == 'new':
                self.box = pygame.image.load('./dialog/wooden_panel_add_new.jpg')
            else:
                self.box = pygame.image.load('./dialog/wooden_panel_reading.jpg')
            self.box = pygame.transform.scale(self.box, (1900, 1060))
            self.x_position = 10
            self.y_position = 10
            self.font = pygame.font.Font('./dialog/dialog_font.ttf',40)
            self.color = (255, 255, 255)
        self.panel = panel
        self.text_index = 0
        self.reading = True
        self.years_to_open = years or 0

    def render(self,screen):
        if self.reading:
            screen.blit(self.box, (self.x_position, self.y_position))
            texts = self.font.render(self.texts[self.text_index],False, self.color)
            screen.blit(texts,(self.x_position + 40, self.y_position + 15))
            if self.panel == 'new':
                years = self.font.render('%s Years' % self.years_to_open, False, self.color)
                screen.blit(years, (1600, 50))

    def next_text(self):
        self.text_index += 1
        if self.text_index >= len(self.texts):
            self.reading = False
            self.text_index = 0
