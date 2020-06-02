import pygame
import sys
import random
import time
from pygame.locals import *

import text_tools
import mysql_connexion

from Classes.Deck import Deck
from Classes.Player import Player
from Classes.Card import Card

pygame.init()
pygame.font.init()



screen = pygame.display.set_mode((1280, 800))
font_title = pygame.font.SysFont('Helvetic', 75)
font_retour = pygame.font.SysFont('Times,Arial', 30)
font_text = pygame.font.SysFont('Times,Arial', 15)
font_text_small = pygame.font.SysFont('Times', 12)

joueur1 = None
joueur2 = None

deck_list_cards = Deck('Liste de toutes les cartes')
deck_joueur1 = None
deck_joueur2 = None
hand1 = {}
hand2 = {}
player1_username = ''
player2_username = ''
rect_end_turn = None
tour = None
deck_len = 32

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

fond_carte_po = pygame.image.load("ressources/fonds de cartes/fond_carte_13.png").convert_alpha()
fond_carte_pm = pygame.image.load("ressources/fonds de cartes/fond_carte_11.png").convert_alpha()
fond_carte_pa = pygame.image.load("ressources/fonds de cartes/fond_carte_09.png").convert_alpha()


fond_carte_po_small = pygame.image.load("ressources/fonds de cartes/fond_carte_13_small.png").convert_alpha()
fond_carte_pm_small = pygame.image.load("ressources/fonds de cartes/fond_carte_11_small.png").convert_alpha()
fond_carte_pa_small = pygame.image.load("ressources/fonds de cartes/fond_carte_09_small.png").convert_alpha()


def game():
    

    global joueur1
    global joueur2
    global tour
    global deck_joueur1
    global deck_joueur2
    global deck_list_cards

    joueur1 = Player(1, '')
    joueur2 = Player(2, '')
    deck_joueur1 = Deck('Deck de test 1')
    deck_joueur2 = Deck('Deck de test 2')

    def add_card_to_hand(deck, joueur, delete=False):
        card_from_hand_to_deck = random.choice(deck.get_cards_from_deck())
        card_to_add = Card(card_from_hand_to_deck[1],
                           card_from_hand_to_deck[2],
                           card_from_hand_to_deck[3],
                           card_from_hand_to_deck[4],
                           card_from_hand_to_deck[5],
                           card_from_hand_to_deck[6],
                           card_from_hand_to_deck[7],
                           card_from_hand_to_deck[8])
        joueur.hand.append(card_to_add)

        if delete:
            deck.del_card_from_deck(card_from_hand_to_deck)

    def end_turn():
        global tour
        print('Fin du tour')
        print('Tour ' + str(tour))

        if tour % 2 == 0:
            rect_end_turn = pygame.Rect(10, 400, 1260, 100)
            
            text_tools.draw_text('Tour ' + str(tour + 1) + ' - C\'est au joueur 1 de jouer !', font_title, (255, 255, 255), screen, 250, 320)
            pygame.display.flip()
            joueur1.add_action_to_stock()
            joueur1.add_gold_to_stock()
            joueur1.add_mana_to_stock()
        elif tour % 2 == 1:
            rect_end_turn = pygame.Rect(10, 400, 1260, 100)
            
            text_tools.draw_text('Tour ' + str(tour + 1) + ' - C\'est au joueur 2 de jouer !', font_title, (255, 255, 255), screen, 250, 320)
            pygame.display.flip()

            joueur2.add_action_to_stock()
            joueur2.add_gold_to_stock()
            joueur2.add_mana_to_stock()
        tour += 1
        time.sleep(2)

    def action_depending_of_card(player, enemy, player_hand, player_deck):
        bonus_damages = 0
        progressing = True
        done = False

        rect_info = pygame.Rect(10, 400, 1260, 100)

        for j in range(0, len(player.get_player_hand())):
            # On joue la carte avec le bouton gauche
            if player_hand[j].collidepoint((mx, my)) and event.button == 1 and player.hand[j]:

                if 25 < enemy.shield < 30:
                    bonus_damages = 0.05
                elif 20 < enemy.shield <= 25:
                    bonus_damages = 0.10
                elif 15 < enemy.shield <= 20:
                    bonus_damages = 0.15
                elif 10 < enemy.shield <= 15:
                    bonus_damages = 0.20
                elif 5 < enemy.shield <= 10:
                    bonus_damages = 0.25
                elif 0 < enemy.shield <= 5:
                    bonus_damages = 0.30

                # print('shield : ' + str(enemy.shield) + ' - bonus dégats : ' + str(bonus_damages))

                if player.hand[j].ressource_type == 'PA':
                    if player.action_stock >= player.hand[j].cost:
                        # print('Vous pouvez jouer la carte')
                        if player.hand[j].effect == 'Shield':
                            if player.hand[j].target == 'Self':
                                if player.shield < 30:
                                    print('Le joueur ' + str(player.player_index) + ' gagne ' + str(player.hand[j].value) + ' points de shield')
                                    player.shield += player.hand[j].value
                                    if player.shield > 30:
                                        player.shield = 30
                                    progressing = False
                                else:
                    
                                    text_tools.draw_text('Vos points de bouclier sont au maximum',
                                                         font_title, (255, 255, 255), screen, 250, 420)
                                    pygame.display.flip()
                                    time.sleep(1)
                            elif enemy.shield > abs(player.hand[j].value):
                                if enemy.shield > 0:
                                    enemy.shield += player.hand[j].value
                                    print('Le joueur ' + str(enemy.player_index) + ' perd ' + str(abs(player.hand[j].value)) + ' points de shield')
                                    if enemy.shield < 0:
                                        enemy.shield = 0
                                    progressing = False
                                else:
                                    
                                    text_tools.draw_text('L\'adversaire n\'a plus de bouclier !',
                                                         font_title, (255, 255, 255), screen, 250, 420)
                                    pygame.display.flip()
                                    time.sleep(1)
                        elif player.hand[j].effect == 'Life':
                            if player.hand[j].target == 'Self':
                                if player.hp < 100:
                                    print('Le joueur ' + str(player.player_index) + ' gagne ' + str(player.hand[j].value) + ' points de vie')
                                    player.hp += player.hand[j].value
                                    if player.hp > 100:
                                        player.hp = 100
                                    progressing = False
                                else:
                                    
                                    text_tools.draw_text('Vos points de vie sont au maximum',
                                                         font_title, (255, 255, 255), screen, 250, 420)
                                    pygame.display.flip()
                                    time.sleep(1)
                            elif enemy.hp > abs(player.hand[j].value):
                                enemy.hp += int(player.hand[j].value * (1 + bonus_damages))
                                print('Le joueur ' + str(enemy.player_index) + ' perd ' + str(abs(int(player.hand[j].value * (1 + bonus_damages)))) + ' points de vie')
                                progressing = False
                            elif enemy.hp <= abs(player.hand[j].value):
                                enemy.hp += int(player.hand[j].value * (1 + bonus_damages))
                                print('Le joueur ' + str(enemy.player_index) + ' perd ' + str(abs(int(player.hand[j].value * (1 + bonus_damages)))) + ' points de vie')
                                print('Le joueur ' + str(enemy.player_index) + ' n\'a plus de points de vie ! Le joueur ' + str(player.player_index) + ' remporte la partie !')
                                done = end_game()
                                return done

                        if progressing == False:
                            player.action_stock -= player.hand[j].cost
                            player.hand.remove(player.hand[j])
                            if player_deck.get_nb_cards_in_deck() > 0:
                                add_card_to_hand(player_deck, player, True)
                            else:
                                
                                text_tools.draw_text('Le joueur n\'a plus de cartes dans son deck !',
                                                     font_title, (255, 255, 255), screen, 250, 420)
                                pygame.display.flip()
                                time.sleep(1)

                            end_turn()
                        # print(str(tour))
                    else:
                
                        text_tools.draw_text('Pas assez de ressouces',
                                             font_title, (255, 255, 255), screen, 250, 320)
                        pygame.display.flip()
                        time.sleep(1)
                elif player.hand[j].ressource_type == 'PM':
                    if player.mana_stock >= player.hand[j].cost:
                        # print('Vous pouvez jouer la carte')
                        if player.hand[j].effect == 'Shield':
                            if player.hand[j].target == 'Self':
                                if player.shield < 30:
                                    print('Le joueur ' + str(player.player_index) + ' gagne ' + str(
                                        player.hand[j].value) + ' points de shield')
                                    player.shield += player.hand[j].value
                                    if player.shield > 30:
                                        player.shield = 30
                                    progressing = False
                                else:
                                    
                                    text_tools.draw_text('Vos points de bouclier sont au maximum',
                                                         font_title, (255, 255, 255), screen, 250, 420)
                                    pygame.display.flip()
                                    time.sleep(1)
                            elif enemy.shield > abs(player.hand[j].value):
                                if enemy.shield > 0:
                                    enemy.shield += player.hand[j].value
                                    print('Le joueur ' + str(enemy.player_index) + ' perd ' + str(
                                        abs(player.hand[j].value)) + ' points de shield')
                                    if enemy.shield < 0:
                                        enemy.shield = 0
                                    progressing = False
                                else:
                                    
                                    text_tools.draw_text('L\'adversaire n\'a plus de bouclier !',
                                                         font_title, (255, 255, 255), screen, 250, 420)
                                    pygame.display.flip()
                                    time.sleep(1)
                        elif player.hand[j].effect == 'Life':
                            if player.hand[j].target == 'Self':
                                if player.hp < 100:
                                    print('Le joueur ' + str(player.player_index) + ' gagne ' + str(
                                        player.hand[j].value) + ' points de vie')
                                    player.hp += player.hand[j].value
                                    if player.hp > 100:
                                        player.hp = 100
                                    progressing = False
                                else:
                                    
                                    text_tools.draw_text('Vos points de vie sont au maximum',
                                                         font_title, (255, 255, 255), screen, 250, 420)
                                    pygame.display.flip()
                                    time.sleep(1)
                            elif enemy.hp > abs(player.hand[j].value):
                                enemy.hp += int(player.hand[j].value * (1 + bonus_damages))
                                print('Le joueur ' + str(enemy.player_index) + ' perd ' + str(abs(int(player.hand[j].value * (1 + bonus_damages)))) + ' points de vie')
                                progressing = False
                            elif enemy.hp <= abs(player.hand[j].value):
                                enemy.hp += int(player.hand[j].value * (1 + bonus_damages))
                                print('Le joueur ' + str(enemy.player_index) + ' perd ' + str(abs(int(player.hand[j].value * (1 + bonus_damages)))) + ' points de vie')
                                print('Le joueur ' + str(enemy.player_index) + ' n\'a plus de points de vie ! Le joueur ' + str(player.player_index) + ' remporte la partie !')
                                done = end_game()
                                return done
                        if progressing == False:
                            player.mana_stock -= player.hand[j].cost
                            player.hand.remove(player.hand[j])
                            if player_deck.get_nb_cards_in_deck() > 0:
                                add_card_to_hand(player_deck, player, True)
                            else:
                                
                                text_tools.draw_text('Le joueur n\'a plus de cartes dans son deck !',
                                                     font_title, (255, 255, 255), screen, 250, 420)
                                pygame.display.flip()
                                time.sleep(1)

                            end_turn()
                        # print(str(tour))
                    else:
                        
                        text_tools.draw_text('Pas assez de ressouces',
                                             font_title, (255, 255, 255), screen, 250, 320)
                        pygame.display.flip()
                        time.sleep(1)
                elif player.hand[j].ressource_type == 'PO':
                    if player.gold_stock >= player.hand[j].cost:
                        # print('Vous pouvez jouer la carte')
                        if player.hand[j].effect == 'Shield':
                            if player.hand[j].target == 'Self':
                                if player.shield < 30:
                                    print('Le joueur ' + str(player.player_index) + ' gagne ' + str(
                                        player.hand[j].value) + ' points de shield')
                                    player.shield += player.hand[j].value
                                    if player.shield > 30:
                                        player.shield = 30
                                    progressing = False
                                else:
                                
                                    text_tools.draw_text('Vos points de bouclier sont au maximum',
                                                         font_title, (255, 255, 255), screen, 250, 420)
                                    pygame.display.flip()
                                    time.sleep(1)
                            elif enemy.shield > abs(player.hand[j].value):
                                if enemy.shield > 0:
                                    enemy.shield += player.hand[j].value
                                    print('Le joueur ' + str(enemy.player_index) + ' perd ' + str(
                                        abs(player.hand[j].value)) + ' points de shield')
                                    if enemy.shield < 0:
                                        enemy.shield = 0
                                    progressing = False
                                else:
                                    
                                    text_tools.draw_text('L\'adversaire n\'a plus de bouclier !',
                                                         font_title, (255, 255, 255), screen, 250, 420)
                                    pygame.display.flip()
                                    time.sleep(1)
                        elif player.hand[j].effect == 'Life':
                            if player.hand[j].target == 'Self':
                                if player.hp < 100:
                                    print('Le joueur ' + str(player.player_index) + ' gagne ' + str(
                                        player.hand[j].value) + ' points de vie')
                                    player.hp += player.hand[j].value
                                    if player.hp > 100:
                                        player.hp = 100
                                    progressing = False
                                else:
                                    
                                    text_tools.draw_text('Vos points de vie sont au maximum',
                                                         font_title, (255, 255, 255), screen, 250, 420)
                                    pygame.display.flip()
                                    time.sleep(1)
                            elif enemy.hp > abs(player.hand[j].value):
                                enemy.hp += int(player.hand[j].value * (1 + bonus_damages))
                                print('Le joueur ' + str(enemy.player_index) + ' perd ' + str(abs(int(player.hand[j].value * (1 + bonus_damages)))) + ' points de vie')
                                progressing = False
                            elif enemy.hp <= abs(player.hand[j].value):
                                enemy.hp += int(player.hand[j].value * (1 + bonus_damages))
                                print('Le joueur ' + str(enemy.player_index) + ' perd ' + str(abs(int(player.hand[j].value * (1 + bonus_damages)))) + ' points de vie')
                                print('Le joueur ' + str(enemy.player_index) + ' n\'a plus de points de vie ! Le joueur ' + str(player.player_index) + ' remporte la partie !')
                                done = end_game()
                                return done

                        if progressing == False:
                            player.gold_stock -= player.hand[j].cost
                            player.hand.remove(player.hand[j])
                            if player_deck.get_nb_cards_in_deck() > 0:
                                add_card_to_hand(player_deck, player, True)
                            else:
                                
                                text_tools.draw_text('Le joueur n\'a plus de cartes dans son deck !',
                                                     font_title, (255, 255, 255), screen, 250, 320)
                                pygame.display.flip()
                                time.sleep(1)

                            end_turn()
                        # print(str(tour))
                    else:
                        
                        text_tools.draw_text('Pas assez de ressouces',
                                             font_title, (255, 255, 255), screen, 250, 320)
                        pygame.display.flip()
                        time.sleep(1)
                # joueur2.hand.remove(joueur2.hand[j])

            # Discard avec le bouton droit
            elif player_hand[j].collidepoint((mx, my)) and event.button == 3 and player.hand[j]:
                print('Clic sur la ' + str(j + 1) + 'eme carte de ma main du joueur ' + str(player.player_index))
                print('discard ' + player.hand[j].name)
                player.hand.remove(player.hand[j])

                if player_deck.get_nb_cards_in_deck() > 0:
                    add_card_to_hand(player_deck, player, True)

                end_turn()
                # print(str(tour))

    usernames = get_username()

    joueur1.change_name(usernames[0])
    joueur2.change_name(usernames[1])
    joueur1.add_action_to_stock()
    joueur1.add_gold_to_stock()
    joueur1.add_mana_to_stock()

    cards = mysql_connexion.readCards()

    for card in cards:
        deck_list_cards.add_card_to_deck(card)

    for i in range(0, deck_len):
        card_from_list_to_deck = random.choice(deck_list_cards.get_cards_from_deck())
        deck_joueur1.add_card_to_deck(card_from_list_to_deck)

        card_from_list_to_deck2 = random.choice(deck_list_cards.get_cards_from_deck())
        deck_joueur2.add_card_to_deck(card_from_list_to_deck2)

    tour = 1

    # On remplit la main de départ des joueurs
    # Main du joueur1
    for i in range(0, 7):
        add_card_to_hand(deck_joueur1, joueur1)
        # deck_joueur1.del_card_from_deck(card_from_hand_to_deck)

    # Main du joueur2
    for j in range(0, 7):
        add_card_to_hand(deck_joueur2, joueur2)

    
    

    continuer = True
    while continuer:
        mx, my = pygame.mouse.get_pos()
        game_interface(joueur1, joueur2)
        print_hand(joueur1)
        print_hand(joueur2)

        # done = end_game()
        # if done:
        #     continuer = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    continuer = False
            if event.type == MOUSEBUTTONDOWN:
                if tour % 2 == 1:
                    done = action_depending_of_card(joueur1, joueur2, hand1, deck_joueur1)
                elif tour % 2 == 0:
                    done = action_depending_of_card(joueur2, joueur1, hand2, deck_joueur2)

                if done:
                    continuer = False

                if rect_end_turn.collidepoint((mx, my)) and event.button == 1:
                    end_turn()
                    # print(str(tour))

        pygame.display.update()


def game_interface(joueur1, joueur2):
    screen.fill((192, 192, 192))
    global rect_end_turn

    rect_joueur_2 = pygame.Rect(10, 0, 1260, 100)
    text_tools.draw_text(joueur2.name, font_title, (0, 0, 0), screen, 35, 25)

    rect_joueur_1 = pygame.Rect(10, 810, 1260, 100)
    text_tools.draw_text(joueur1.name, font_title, (0, 0, 0), screen, 35, 735)

    text_tools.draw_text('Tour ' + str(tour), font_text, (0, 0, 0), screen, 25, 440)

    rect_end_turn = pygame.Rect(1140, 425, 100, 50)
    text_tools.draw_text('Fin de tour', font_text, (0, 0, 0), screen, 1155, 440)

    text_tools.draw_text(str(joueur2.hp), font_text, (0, 0, 0), screen, 460, 60)
    screen.blit(heart_small, (450, 20))
    text_tools.draw_text(str(joueur1.hp), font_text, (0, 0, 0), screen, 460, 770)
    screen.blit(heart_small, (450, 730))

    text_tools.draw_text(str(joueur2.shield), font_text, (0, 0, 0), screen, 535, 60)
    screen.blit(shield_small, (525, 20))
    text_tools.draw_text(str(joueur1.shield), font_text, (0, 0, 0), screen, 535, 770)
    screen.blit(shield_small, (525, 730))

    text_tools.draw_text(str(joueur2.mana_stock), font_text, (0, 0, 0), screen, 745, 60)
    text_tools.draw_text('(+' + str(joueur2.mana_generation) + ')', font_text, (0, 0, 0), screen, 760, 60)
    screen.blit(pm_small, (750, 20))
    text_tools.draw_text(str(joueur1.mana_stock), font_text, (0, 0, 0), screen, 745, 770)
    text_tools.draw_text('(+' + str(joueur1.mana_generation) + ')', font_text, (0, 0, 0), screen, 760, 870)
    screen.blit(pm_small, (750, 730))

    text_tools.draw_text(str(joueur2.gold_stock), font_text, (0, 0, 0), screen, 815, 60)
    text_tools.draw_text('(+' + str(joueur2.gold_generation) + ')', font_text, (0, 0, 0), screen, 835, 60)
    screen.blit(po_small, (825, 20))
    text_tools.draw_text(str(joueur1.gold_stock), font_text, (0, 0, 0), screen, 815, 770)
    text_tools.draw_text('(+' + str(joueur1.gold_generation) + ')', font_text, (0, 0, 0), screen, 835, 870)
    screen.blit(po_small, (825, 730))

    text_tools.draw_text(str(joueur2.action_stock), font_text, (0, 0, 0), screen, 890, 60)
    text_tools.draw_text('(+' + str(joueur2.action_generation) + ')', font_text, (0, 0, 0), screen, 910, 60)
    screen.blit(pa_small, (900, 20))
    text_tools.draw_text(str(joueur1.action_stock), font_text, (0, 0, 0), screen, 890, 770)
    text_tools.draw_text('(+' + str(joueur1.action_generation) + ')', font_text, (0, 0, 0), screen, 910, 870)
    screen.blit(pa_small, (900, 730))

    text_tools.draw_text(str(deck_joueur2.get_nb_cards_in_deck()) + ' card(s) left', font_text, (0, 0, 0), screen, 1100,
                         60)
    screen.blit(deck_small, (1120, 20))
    text_tools.draw_text(str(deck_joueur1.get_nb_cards_in_deck()) + ' card(s) left', font_text, (0, 0, 0), screen, 1100,
                         770)
    screen.blit(deck_small, (1120, 730))


def print_hand(joueur):
    position = joueur.get_player_index()
    player_hand = joueur.get_player_hand()
    global hand1
    global hand2

    if position == 1:
        x = 50
        y = 485

        for i in range(0, len(joueur.get_player_hand())):
            hand1[i] = pygame.Rect(x, y, 150, 200)
            pygame.draw.rect(screen, (192, 192, 192), hand1[i])

            text_tools.draw_text("Coût :", font_text, (0, 0, 0), screen, x + 15, y + 50)
            text_tools.draw_text(str(player_hand[i].cost), font_text, (0, 0, 0), screen, x + 67, y + 50)
            if player_hand[i].ressource_type == 'PA':
                screen.blit(fond_carte_pa_small, (x, y))
                screen.blit(pa_very_small, (x+105, y+52))
            elif player_hand[i].ressource_type == 'PO':
                screen.blit(fond_carte_po_small, (x, y))
                screen.blit(po_very_small, (x+105, y+52))
            elif player_hand[i].ressource_type == 'PM':
                screen.blit(fond_carte_pm_small, (x, y))
                screen.blit(pm_very_small, (x+105, y+52))

            text_tools.draw_text(player_hand[i].name, font_text_small, (0, 0, 0), screen, x + 12, y + 5)

            text_tools.draw_text(player_hand[i].target, font_text, (0, 0, 0), screen, x + 15, y + 100)
            text_tools.draw_text(str(player_hand[i].value), font_text, (0, 0, 0), screen, x + 67, y + 100)
            if player_hand[i].effect == 'Shield':
                screen.blit(shield_very_small, (x+105, y+102))
            elif player_hand[i].effect == 'Life':
                screen.blit(heart_very_small, (x+105, y+102))

            x += 175

    elif position == 2:
        x = 50
        y = 85

        for i in range(0, len(joueur.get_player_hand())):
            hand2[i] = pygame.Rect(x, y, 150, 200)
            pygame.draw.rect(screen, (192, 192, 192), hand2[i])

            text_tools.draw_text("Coût :", font_text, (0, 0, 0), screen, x + 15, y + 50)
            text_tools.draw_text(str(player_hand[i].cost), font_text, (0, 0, 0), screen, x + 67, y + 50)
            if player_hand[i].ressource_type == 'PA':
                screen.blit(fond_carte_pa_small, (x, y))
                screen.blit(pa_very_small, (x + 105, y + 52))
            elif player_hand[i].ressource_type == 'PO':
                screen.blit(fond_carte_po_small, (x, y))
                screen.blit(po_very_small, (x + 105, y + 52))
            elif player_hand[i].ressource_type == 'PM':
                screen.blit(fond_carte_pm_small, (x, y))
                screen.blit(pm_very_small, (x + 105, y + 52))

            text_tools.draw_text(player_hand[i].name, font_text_small, (0, 0, 0), screen, x + 12, y + 5)

            text_tools.draw_text(player_hand[i].target, font_text, (0, 0, 0), screen, x + 15, y + 100)
            text_tools.draw_text(str(player_hand[i].value), font_text, (0, 0, 0), screen, x + 67, y + 100)
            if player_hand[i].effect == 'Shield':
                screen.blit(shield_very_small, (x + 105, y + 102))
            elif player_hand[i].effect == 'Life':
                screen.blit(heart_very_small, (x + 105, y + 102))

            x += 175


def get_username():
    font = pygame.font.Font(None, 70)
    input_box_1 = pygame.Rect(500, 350, 350, 65)
    input_box_2 = pygame.Rect(500, 450, 350, 65)
    button_play = pygame.Rect(500, 700, 250, 65)
    color_inactive = pygame.Color('white')
    color_active = pygame.Color('red')
    color1 = color_inactive
    color2 = color_inactive
    global player1_username
    global player2_username
    active1 = False
    active2 = False
    text1 = ''
    text2 = ''
    done = False

    while not done:
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box_1.collidepoint(mx, my):
                    # Toggle the active variable.
                    active1 = not active1
                    if active2:
                        active2 = False
                elif input_box_2.collidepoint(mx, my):
                    # Toggle the active variable.
                    active2 = not active2
                    if active1:
                        active1 = False
                else:
                    active1 = False
                    active2 = False
                # Change the current color of the input box.
                color1 = color_active if active1 else color_inactive
                color2 = color_active if active2 else color_inactive
            if event.type == pygame.KEYDOWN:
                if active1:
                    if event.key == pygame.K_RETURN:
                        player1_username = text1
                    elif event.key == pygame.K_BACKSPACE:
                        text1 = text1[:-1]
                    else:
                        text1 += event.unicode
                if active2:
                    if event.key == pygame.K_RETURN:
                        player2_username = text2
                    elif event.key == pygame.K_BACKSPACE:
                        text2 = text2[:-1]
                    else:
                        text2 += event.unicode
            if event.type == MOUSEBUTTONDOWN:
                if button_play.collidepoint(mx, my) and event.button == 1 and text1 != '' and text2 != '':
                    return [text1, text2]

        screen.fill((121, 114, 114))
        # Render the current text.
        text_tools.draw_text("Clic gauche pour jouer une carte, clic droit pour se défausser d'une carte",
                             font_text, (255, 255, 255), screen, 50, 80)
        text_tools.draw_text("Pseudo joueur 1 :", font, pygame.Color('white'), screen, 50, 350)
        text_tools.draw_text("Pseudo joueur 2 :", font, pygame.Color('white'), screen, 50, 450)
        txt_surface = font.render(text1, True, color1)
        txt_surface2 = font.render(text2, True, color2)
        # Resize the box if the text is too long.
        width = max(350, txt_surface.get_width() + 10)
        input_box_1.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box_1.x + 5, input_box_1.y + 5))
        screen.blit(txt_surface2, (input_box_2.x + 5, input_box_2.y + 5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color1, input_box_1, 2)
        pygame.draw.rect(screen, color2, input_box_2, 2)

        pygame.draw.rect(screen, (121, 114, 114), button_play)
        text_tools.draw_text('JOUER', font_title, (255, 255, 255), screen, 500, 705)

        pygame.display.flip()

def end_game():
    global joueur1
    global joueur2

    button_retour = pygame.Rect(400, 800, 400, 65)
    done = False
    musique_partie.stop()

    screen.fill((30, 30, 30))

    # joueur1.hp = 0

    text_tools.draw_text("Nombre de tour joués : " + str(tour), font_retour, (255, 255, 255), screen, 120, 300)
    pygame.draw.rect(screen, (30, 30, 30), button_retour)
    text_tools.draw_text('Retour au menu', font_title, (255, 255, 255), screen, 400, 805)

    if joueur1.hp <= 0:
        text_tools.draw_text("Victoire du joueur 2 !", font_title, (255, 255, 255), screen, 400, 120)
        text_tools.draw_text("Nombre de Points de vie restants : " + str(joueur2.hp), font_retour, (255, 255, 255),
                             screen, 120, 400)
        text_tools.draw_text("Nombre de points de bouclier restants : " + str(joueur1.shield), font_retour,
                             (255, 255, 255), screen, 120, 500)
        musique_loose_start.play()
        musique_loose.play()
    elif joueur2.hp <= 0:
        text_tools.draw_text("Victoire du joueur 1 !", font_title, (255, 255, 255), screen, 400, 120)
        text_tools.draw_text("Nombre de Points de vie restants : " + str(joueur1.hp), font_retour, (255, 255, 255),
                             screen, 120, 400)
        text_tools.draw_text("Nombre de points de bouclier restants : " + str(joueur1.shield), font_retour,
                             (255, 255, 255), screen, 120, 500)
        musique_win_start.play()
        musique_win.play()
    pygame.display.flip()

    while not done:
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if button_retour.collidepoint(mx, my) and event.button == 1:
                    done = True
                    return done
            if event.type == QUIT:
                pygame.quit()
                sys.exit()