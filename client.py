import time
import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.48"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.cards = self.connect()

    def get_cards(self):
        return self.cards

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)


class Player:
    def __init__(self, cards):
        self.cards = cards

    def show_cards(self):
        print("Your cards:", end=" ")
        for card in self.cards:
            print(card, end=" ")
        print()

    def pass_card(self):
        n = int(input("Select a card to pass: "))
        self.cards.pop(n-1)
        self.show_cards()


def read_cards(cards):
    cards = cards.split(" ")
    return cards


def main():
    n = Network()
    initial_cards = read_cards(n.get_cards())
    p = Player(initial_cards)
    p.show_cards()
    p.pass_card()

    while True:
        time.sleep(60)
        break


main()
