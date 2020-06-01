class Player:
    def __init__(self, index, name):
        # Joueur 1 ou Joueur 2
        self.player_index = index
        self.name = name
        self.hp = 100
        self.shield = 30
        # Tableau qui contient la main du joueur - 7 cartes max
        self.hand = []
        self.gold_generation = 1
        self.gold_stock = 0
        self.mana_generation = 1
        self.mana_stock = 0
        self.action_generation = 1
        self.action_stock = 0

    def change_name(self, name):
        self.name = name

    def change_hP(self, hp_change):
        self.hp = self.hp - hp_change
        print("Vous avez actuellement " + self.hp + " pvs !")

    def change_shield(self, shield_change):
        self.shield = self.shield - shield_change
        print("Vous avez actuellement " + self.shield + " points de bouclier !")

    def get_player_index(self):
        return self.player_index

    def get_player_hand(self):
        return self.hand

    def add_gold_to_stock(self):
        self.gold_stock = self.gold_stock + self.gold_generation

    def add_mana_to_stock(self):
        self.mana_stock = self.mana_stock + self.mana_generation

    def add_action_to_stock(self):
        self.action_stock = self.action_stock + self.action_generation
