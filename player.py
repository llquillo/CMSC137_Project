class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.cards = []

    def get_player_id(self):
        return self.player_id

    def add_card(self, card):
        self.cards.append(str(card))

    def pass_card(self, card_no):
        return self.cards.pop(card_no)

    def show_cards(self):
        print("Player", self.player_id, "cards:", end=" ")
        for card in self.cards:
            print(card, end=" ")
        print()

    def win(self):
        if len(self.cards) == 4:
            return all(str(x)[0] == str(self.cards[0])[0] for x in self.cards)
        else:
            return False
