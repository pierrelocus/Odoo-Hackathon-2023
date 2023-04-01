import pygame


class DialogBox:

    X_POSITION = 600
    Y_POSITION = 600
    def __init__(self):
        self.box = pygame.image.load('./dialog/dialogs_box.png')
        pygame.transform.scale(self.box,(700,100))
        self.texts = ["HOOOOOOOOOOO","caca"]
        self.text_index = 0
        self.font = pygame.font.Font('./dialog/dialog_font.ttf',18)
        self.reading = True

    def render(self,screen):
        if self.reading:
            screen.blit(self.box,(self.X_POSITION,self.Y_POSITION))
            texts = self.font.render(self.texts[self.text_index],False,(0,0,0))
            screen.blit(texts,(self.X_POSITION,self.Y_POSITION))

    def next_text(self):
        self.text_index += 1
        if self.text_index >= len(self.texts):
            self.reading = False
