import sys
import pygame
from pygame.locals import *

import text_tools, play, Cards_CRUD, mysql_connexion

mysql_connexion.init_db()

pygame.init()
pygame.font.init()

pygame.display.set_caption('Projet Dev')
screen = pygame.display.set_mode((1280, 800),FULLSCREEN)
fond_ecran = pygame.image.load("ressources/images/chateau2.jpg")
font_title = pygame.font.SysFont('Helvetic', 75)
font_text = pygame.font.SysFont('Times,Arial', 20)

heart = pygame.image.load("ressources/images/heart.png").convert_alpha()
heart_small = pygame.transform.scale(heart, (44, 40))
heart_very_small = pygame.transform.scale(heart, (25, 23))

shield = pygame.image.load("ressources/images/shield.png").convert_alpha()
shield_small = pygame.transform.scale(shield, (40, 40))
shield_very_small = pygame.transform.scale(shield, (23, 23))

pm = pygame.image.load("ressources/images/potion-icon.jpg").convert_alpha()
pm_small = pygame.transform.scale(pm, (40, 40))
pm_very_small = pygame.transform.scale(pm, (23, 23))

po = pygame.image.load("ressources/images/or-icon.png").convert_alpha()
po_small = pygame.transform.scale(po, (40, 40))
po_very_small = pygame.transform.scale(po, (23, 23))

pa = pygame.image.load("ressources/images/attaque-icon.jpg").convert_alpha()
pa_small = pygame.transform.scale(pa, (40, 40))
pa_very_small = pygame.transform.scale(pa, (23, 23))

deck = pygame.image.load("ressources/images/cards-icon.png").convert_alpha()
deck_small = pygame.transform.scale(deck, (40, 40))
deck_very_small = pygame.transform.scale(deck, (23, 23))


def main_menu():
    click = False

    while True:
        screen.fill((192, 192, 192))
        screen.blit(fond_ecran,(25,25))
        text_tools.draw_text('Projet Dev', font_title, (0, 0, 0), screen, 50, 20)
        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(50, 200, 300, 100)
        button_2 = pygame.Rect(50, 350, 300, 100)
        button_3 = pygame.Rect(50, 500, 300, 100)
        button_4 = pygame.Rect(50, 650, 300, 100)
        
        if button_1.collidepoint(mx, my):
            if click:
                play.game()
        if button_2.collidepoint(mx, my):
            if click:
                rules()
        if button_3.collidepoint(mx, my):
            if click:
                options()
        if button_4.collidepoint(mx, my):
            if click:
                exit()

        pygame.draw.rect(screen, (0, 0, 0), button_1)
        pygame.draw.rect(screen, (0, 0, 0), button_2)
        pygame.draw.rect(screen, (0, 0, 0), button_3)
        pygame.draw.rect(screen, (0, 0, 0), button_4)

        screen.blit(font_title.render('Jouer', True, (255, 255, 255)), (88, 225))
        screen.blit(font_title.render('Regles', True, (255, 255, 255)), (88, 375))
        screen.blit(font_title.render('Options', True, (255, 255, 255)), (88, 525))
        screen.blit(font_title.render('Quitter', True, (255, 255, 255)), (88, 675))

        text_tools.blit_text(screen, """Cliquer sur le bouton 
que vous voulez et appuyer sur \'Echap\' 
pour revenir au menu precedent""", (1105, 385), font_text, (0, 6, 251))

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


def exit() :
    pygame.quit()
    
    
def rules():
    continuer = True
    while continuer:
        screen.fill((192, 192, 192))
        mx, my = pygame.mouse.get_pos()

        text_tools.draw_text('Regles', font_title, (0, 0, 0), screen, 20, 20)

        rules = """Le but du jeu est de vider la barre de vie de son adversaire ainsi etre le dernier survivant.
Chaque joueur possede un maximum de 100 PV (barre de vie) et de 30 points de boucliers. 

Plus votre bouclier prend de degats plus vous perdez de vos PV.

Vous avez un deck de 32 cartes maximun et une main de 7 cartes maximum.

Vous disposez de 3 ressources différentes, nécessaires à l'utilisation de vos cartes : 
    - votre energie
    - vos potions
    - votre mana
    
Vos ressources sont generees automatiquement a chaque debut de tour (ou a l'aide de vos cartes selon ces competences).

Deroulement d'un tour : 
    
Au debut de votre tour, vous generez des ressources en plus.
Apres cela, vous piochez une carte aleatoirement dans votre deck si votre en main ne contient pas deja 7 cartes.
Vous avez en suite 2 choix :
    - Soit vous jouez une carte avec clique gauche en depensant le cout necessaire en ressources.
    - Soit vous defaussez une carte de votre main.
    
C'est la fin de votre tour, et le debut de celui de votre adversaire qui se deroule exactement pareil.

La partie se terminent lorsqu'un joueur tombe a 0 points de vie.
"""

        text_tools.blit_text(screen, rules, (20, 120), font_text)

        button_option_1 = pygame.Rect(20, 850, 100, 40)
        pygame.draw.rect(screen, (0, 0, 0), button_option_1)
        text_tools.draw_text('Retour', font_text, (255, 255, 255), screen, 32, 855)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    continuer = False
            if event.type == MOUSEBUTTONDOWN:
                if button_option_1.collidepoint(mx, my) and event.button == 1:
                    continuer = False

        pygame.display.update()


def options():
    continuer = True
    click = False

    while continuer:
        screen.fill((192, 192, 192))
        mx, my = pygame.mouse.get_pos()


        text_tools.draw_text('Options', font_title, (0, 0, 0), screen, 20, 20)
        button_option_1 = pygame.Rect(50, 200, 600, 100)
        button_option_3 = pygame.Rect(50, 500, 600, 100)

        if button_option_1.collidepoint(mx, my):
            if click:
                Cards_CRUD.cards_list()
        elif button_option_3.collidepoint(mx, my):
            if click:
                continuer = False

        pygame.draw.rect(screen, (0, 0, 0), button_option_1)
        pygame.draw.rect(screen, (0, 0, 0), button_option_3)

        screen.blit(font_title.render('Gestion des cartes', True, (255, 255, 255)), (88, 225))
        screen.blit(font_title.render('Retour', True, (255, 255, 255)), (88, 525))

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_KP_ENTER):
                    continuer = False
                    break
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


def end_game():
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


main_menu()
