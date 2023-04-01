import pygame


class DialogBox:
    x_position = 300
    y_position = 400
    def __init__(self):

        self.box = pygame.image.load('./dialog/dialogs_box.png')
        self.box = pygame.transform.scale(self.box, (550, 50))
        self.texts = ["haha", "heheh"]
        self.font = pygame.font.Font('./dialog/dialog_font.ttf',18)
        self.text_index = 0
        self.reading = True


    def render(self,screen):
        if self.reading:
            screen.blit(self.box, (self.x_position, self.y_position))
            text = self.font.render(self.texts[self.text_index],False,(0,0,0))
            screen.blit(text, (self.x_position, self.y_position))


    def next_text(self):
        self.text_index += 1
        if self.text_index >= len(self.texts):
            self.reading = False
            self.text_index = 0
