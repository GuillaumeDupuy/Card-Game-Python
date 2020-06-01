# -*- coding: utf-8 -*-

import pygame as pg


pg.init()
screen = pg.display.set_mode((640, 480))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)
COLOR_INVALID = pg.Color('firebrick3')
COLOR_VALID = pg.Color('palegreen3')
WARNING_EMPTY = 'Ne peut pas être nul'
WARNING_INT = 'Doit être un chiffre'
WARNING_STR = 'Doit être une chaine de caractères'

class InputBox:

    def __init__(self, x, y, w, h, text='', input_type='', rules=[], warning_text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.valid = False
        self.rules=rules
        self.warning_text = warning_text
        self.input_type = input_type

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False

            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

    def getInput(self):
        return self.text
        
    def setValid(self, new_valid):
        self.valid = new_valid

    def getValid(self):
        return self.valid

    def validateInput(self):
        print(self.text)
        if self.input_type == int:
            try:
                int(self.getInput())
            except ValueError:
                self.valid = False
                self.color = COLOR_INVALID
                self.text = WARNING_INT
                self.txt_surface = FONT.render(self.text, True, self.color)
                return False
        for rule in self.rules:
            if self.getInput() == rule:
                self.valid = True
                self.color = COLOR_INACTIVE
                self.txt_surface = FONT.render(self.text, True, self.color)
                return True
        if self.getInput() == '':
            self.valid = False
            self.color = COLOR_INVALID
            self.text = WARNING_EMPTY
            self.txt_surface = FONT.render(self.text, True, self.color)
            return False
        if self.rules != []:
            self.valid = False
            self.text = self.warning_text
            self.color = COLOR_INVALID
            self.txt_surface = FONT.render(self.text, True, self.color)
            return False
        self.valid = True
        self.color = COLOR_INACTIVE
        self.txt_surface = FONT.render(self.text, True, self.color)
        return True
    
    
    
    
    
    
    
        
        
        