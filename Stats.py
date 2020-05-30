import sys
import pygame
from pygame.locals import *

screen = pygame.display.set_mode((1280, 910))


def stats():
    running = True
    while running:
        screen.fill((192, 192, 192))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
