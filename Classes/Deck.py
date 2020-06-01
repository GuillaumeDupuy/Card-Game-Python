class Deck:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def reset_deck(self):
        self.cards = []

    def add_card_to_deck(self, card):
        self.cards.append(card)

    def get_cards_from_deck(self):
        return self.cards

    def del_card_from_deck(self, card):
        self.cards.remove(card)

    def get_nb_cards_in_deck(self):
        return len(self.cards)

