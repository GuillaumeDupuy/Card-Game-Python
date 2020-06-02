import sys
import pygame
import csv
import os
from pygame.locals import *

import mysql_connexion
import text_tools
from Classes.Card import Card
from Classes.InputBox import InputBox
from tempfile import NamedTemporaryFile


screen = pygame.display.set_mode((1280, 910))
card_cadre = pygame.display.set_mode((275, 350))
# font_text = pygame.font.SysFont('Comic Sans MS', 20)

cards = []
font_text = pygame.font.SysFont('Comic Sans MS,Arial', 20)
font_title = pygame.font.SysFont('Helvetic', 75)


def cards_list():
    continuer = True

    # begin of the loop
    n = 0
    # end of the loop
    m = 3

    # get_cards_csv()
    # for card in cards:
    #     print(card)

    test_cards = mysql_connexion.readCards()
    get_cards_db(test_cards)
    nb_cards = len(cards)

    while continuer:
        mx, my = pygame.mouse.get_pos()
        screen.fill((192, 192, 192))

        button_option_1 = pygame.Rect(20, 20, 100, 40)
        #pygame.draw.rect(screen, (0, 0, 0), button_option_1)
        #text_tools.draw_text('Retour', font_text, (255, 255, 255), screen, 35, 25)

        button_option_2 = pygame.Rect(20, 820, 150, 40)

        pygame.draw.rect(screen, (255, 0, 0), button_option_1)
        pygame.draw.rect(screen, (255, 0, 0), button_option_2)

        text_tools.draw_text('Retour', font_text, (0, 0, 0), screen, 35, 25)
        text_tools.draw_text('Créer carte', font_text, (0, 0, 0), screen, 35, 825)

        button_edit_1 = pygame.Rect(150, 720, 100, 40)
        button_delete_1 = pygame.Rect(270, 720, 140, 40)
        button_edit_2 = pygame.Rect(500, 720, 100, 40)
        button_delete_2 = pygame.Rect(620, 720, 140, 40)       
        button_edit_3 = pygame.Rect(850, 720, 100, 40)
        button_delete_3 = pygame.Rect(970, 720, 140, 40)
        
        #
        # add_buttons(screen, button_edit_1, button_delete_1, 110)
        # add_buttons(screen, button_edit_2, button_delete_2, 460)
        # add_buttons(screen, button_edit_3, button_delete_3, 810)

        #cards = mysql_connexion.readCards()
        #nb_cards = len(cards)


        fond_carte_po = pygame.image.load("ressources/fonds de cartes/fond_carte_13.png").convert_alpha()
        fond_carte_pm = pygame.image.load("ressources/fonds de cartes/fond_carte_11.png").convert_alpha()
        fond_carte_pa = pygame.image.load("ressources/fonds de cartes/fond_carte_09.png").convert_alpha()

        left_arrow = pygame.image.load("ressources/images/left arrow.png").convert_alpha()
        left_arrow_small = pygame.transform.scale(left_arrow, (50, 50))
        button_left_arrow = pygame.Rect(5, 430, 50, 50)
        pygame.draw.rect(screen, (192, 192, 192), button_left_arrow)

        right_arrow = pygame.image.load("ressources/images/right arrow.png").convert_alpha()
        right_arrow_small = pygame.transform.scale(right_arrow, (50, 50))
        button_right_arrow = pygame.Rect(1225, 430, 50, 50)
        pygame.draw.rect(screen, (192, 192, 192), button_right_arrow)

        x = 110
        y = 200

        # On veut afficher juste 3 cartes à la fois
        for card in cards[n:m]:

            add_buttons(screen, button_edit_1, button_delete_1, 110)
            if len(cards) > n+1:
                add_buttons(screen, button_edit_2, button_delete_2, 460)
            if len(cards) > n+2:
                add_buttons(screen, button_edit_3, button_delete_3, 810)

            # card_set[card[0]] = pygame.Rect(x, y, 340, 474)
            # pygame.draw.rect(screen, (192, 192, 192), card_set[card[0]])

            if card.get_ressource_type() == "PO":
                screen.blit(fond_carte_po, (x, y))
            elif card.get_ressource_type() == "PM":
                screen.blit(fond_carte_pm, (x, y))
            elif card.get_ressource_type() == "PA":
                screen.blit(fond_carte_pa, (x, y))

            if n > 0:
                screen.blit(left_arrow_small, (5, 430))
            if nb_cards > n+3:
                screen.blit(right_arrow_small, (1225, 430))

            
            text_tools.draw_text(card.get_name(), font_text, (0, 0, 0), screen, x+50, y+20)
            text_tools.draw_text('Cost : ' + str(card.get_cost()) + ' ' + card.get_ressource_type(), font_text, (0, 0, 0), screen, x+50, y+100)
            text_tools.draw_text('Effect : ' + str(card.get_value()) + ' ' + card.get_target() + ' ' + card.get_effect(), font_text, (0, 0, 0), screen, x+50, y+125)
            text_tools.draw_text('Rarity : ' + card.get_rarity(), font_text, (0, 0, 0), screen, x+50, y+150)
            y2=400
            for line in break_text(card.get_description()):       
                text_tools.draw_text(line, font_text, (0, 0, 0), screen, x+50, y2)
                y2 = y2 + 25
            

            x += 350

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
                if button_option_2.collidepoint(mx, my) and event.button == 1:
                    new_card = Card('', '', '', '', '', '', '', '')
                    create_card(new_card, "create")
                
                if button_left_arrow.collidepoint(mx, my) and event.button == 1 and n > 0:
                    n = n - 3
                    m = m - 3
                elif button_right_arrow.collidepoint(mx, my) and event.button == 1 and nb_cards > n+3:
                    n = n + 3
                    m = m + 3
                if button_edit_1.collidepoint(mx, my) and event.button == 1:
                    create_card(cards[n], "edit")
                if button_edit_2.collidepoint(mx, my) and event.button == 1:
                    create_card(cards[n+1], "edit")
                if button_edit_3.collidepoint(mx, my) and event.button == 1:
                    create_card(cards[n+2], "edit")                
                if button_delete_1.collidepoint(mx, my) and event.button == 1:
                    delete_card(cards[n])
                if button_delete_2.collidepoint(mx, my) and event.button == 1:
                    delete_card(cards[n+1])
                if button_delete_3.collidepoint(mx, my) and event.button == 1:
                    delete_card(cards[n+2])                


        pygame.display.update()


def create_card(card, mode = "create"):
    name_input = InputBox(200, 25, 140, 32, card.get_name(), str)
    ressource_type_input = InputBox(350, 75, 140, 32, card.get_ressource_type(), str, ['PA', 'PM', 'PO'], 'Ressource non reconnue')
    cost_input = InputBox(100, 125, 140, 32, str(card.get_cost()), int)
    effect_input = InputBox(300, 175, 140, 32, card.get_effect(), str, ['Life', 'Shield'], 'Effet non reconnu')
    value_input = InputBox(100, 225, 140, 32, str(card.get_value()), int)
    target_input = InputBox(250, 275, 140, 32, card.get_target(), str, ['Self', 'Enemy'], 'Cible non reconnue')
    rarity_input = InputBox(350, 325, 140, 32, card.get_rarity(), str, ['Rare', 'Epic', 'Legendary'], 'Rareté non reconnue')
    description_input = InputBox(200, 375, 140, 32, card.get_description(), str)

    input_boxes = [name_input, ressource_type_input, cost_input, effect_input, value_input, target_input, rarity_input, description_input]
    
    clock = pygame.time.Clock()
    done = False

    while not done:
        mx, my = pygame.mouse.get_pos()
        screen.fill((192, 192, 192))

        for box in input_boxes:
            box.update()

        for box in input_boxes:
            box.draw(screen)

        text_tools.draw_text('Nom de la carte:', font_text, (0, 0, 0), screen, 10, 25)
        text_tools.draw_text('Type de ressource (PA, PM ou PO):', font_text, (0, 0, 0), screen, 10, 75)
        text_tools.draw_text('Cout:', font_text, (0, 0, 0), screen, 10, 125)
        text_tools.draw_text('Effet (Life ou Shield):', font_text, (0, 0, 0), screen, 10, 175)
        text_tools.draw_text('Valeur:', font_text, (0, 0, 0), screen, 10, 225)
        text_tools.draw_text('Cible (Self ou Enemy):', font_text, (0, 0, 0), screen, 10, 275)
        text_tools.draw_text('Rareté (Rare, Epic ou Legendary):', font_text, (0, 0, 0), screen, 10, 325)
        text_tools.draw_text('Description:', font_text, (0, 0, 0), screen, 10, 375)


        button_option_1 = pygame.Rect(20, 620, 150, 40)
        button_option_2 = pygame.Rect(220, 620, 150, 40)

        pygame.draw.rect(screen, (255, 0, 0), button_option_1)
        pygame.draw.rect(screen, (255, 0, 0), button_option_2)
        
        text_tools.draw_text(mode, font_text, (0, 0, 0), screen, 35, 625)
        text_tools.draw_text('Retour', font_text, (0, 0, 0), screen, 235, 625)


        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if button_option_1.collidepoint(mx, my) and event.button == 1:
                    for box in input_boxes:
                        box.validateInput()
                    if (mode == "create"):
                        done = mysql_connexion.createCard(input_boxes)
                        
                    elif (mode == "edit"):
                        mysql_connexion.editCard(input_boxes, card.get_name())
                        done = edit_card(input_boxes)
                if button_option_2.collidepoint(mx, my) and event.button == 1:
                    done = True
            for box in input_boxes:
                box.handle_event(event)
            
    
        pygame.display.update()
           


def get_cards_csv():
    with open(card_csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            card = Card(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            cards.append(card)
    csv_file.close()


def get_cards_db(cards_db):
    global cards
    cards = []

    for card_db in cards_db:
        card = Card(card_db[1], card_db[2], card_db[3], card_db[4], card_db[5], card_db[6], card_db[7], card_db[8])
        cards.append(card)


def generate_card(input_boxes):
    validated = validate_boxes(input_boxes)
    if validated == False:
        return False
    
    new_card = Card(input_boxes[0].getInput(), input_boxes[1].getInput(), input_boxes[2].getInput(), input_boxes[3].getInput(), input_boxes[4].getInput(), input_boxes[5].getInput(), input_boxes[6].getInput(), input_boxes[7].getInput())
    cards.append(new_card)
     
    return True


def save_card(card):
    print("new card")

    with open(card_csv_path, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([card.get_name(), card.get_ressource_type(), int(card.get_cost()), card.get_effect(), int(card.get_value()), card.get_target(), card.get_rarity(), card.get_description()])
    csv_file.close()
    
    
def break_text(txt):
    words = txt.split()
    line = ""
    new_txt = []
    x = 0
    for word in words:
        x = x + len(word)
        line = line + word + " "
        if x > 15:
            x = 0
            new_txt.append(line)
            line = ""
    new_txt.append(line)
    return new_txt


def add_buttons(screen, button_edit, button_delete, x):
    y = 725

    pygame.draw.rect(screen, (255, 0, 0), button_edit)
    pygame.draw.rect(screen, (255, 0, 0), button_delete)

    text_tools.draw_text('Modifier', font_text, (0, 0, 0), screen, x+50, y)
    text_tools.draw_text('Supprimer', font_text, (0, 0, 0), screen, x+170, y)
    

def edit_card(input_boxes):
    print("edition d'une carte")
    validated = validate_boxes(input_boxes)
    if validated == False:
        return False
    
    edited_card = Card(input_boxes[0].getInput(), input_boxes[1].getInput(), input_boxes[2].getInput(), input_boxes[3].getInput(), input_boxes[4].getInput(), input_boxes[5].getInput(), input_boxes[6].getInput(), input_boxes[7].getInput())
    
    print(edited_card.get_name())

    
    
    n = find_card_index(edited_card.get_name())
    if n:
        cards[n] = edited_card
        edit_csv()
   
    return True

        
def delete_card(card):
    cards.remove(card)
    mysql_connexion.deleteCard(card.name)


    
def find_card_index(card_name):
    i = 0
    while i < len(cards):
        if cards[i].get_name() == card_name:
            return i
        i+=1
    return False

def validate_boxes(input_boxes):
    for box in input_boxes:
        if not box.getValid():
            return False
    return True

def edit_csv():
    os.remove(card_csv_path)
    with open(card_csv_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for card in cards:
            writer.writerow([card.get_name(), card.get_ressource_type(), int(card.get_cost()), card.get_effect(), int(card.get_value()), card.get_target(), card.get_rarity(), card.get_description()])
    csv_file.close()
