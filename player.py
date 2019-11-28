class Player:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(str(card))

    def show_cards(self):
        print("Your cards:", end=" ")
        for card in self.cards:
            print(card, end=" ")
        print()

    def pass_card(self):
        n = int(input("Select a card to pass [1-4]: "))
        self.cards.pop(n-1)