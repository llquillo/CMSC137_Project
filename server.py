import socket
from _thread import *
import random
import time

max_players = 3

suits = ['C', 'D', 'H', 'S']
ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']

rank_lookup = {}
for i in range(max_players):
    rank_lookup[ranks[i]] = i


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return "".join((self.rank, self.suit))


class Deck:
    def __init__(self):
        self.cards = [Card(r, s) for r in rank_lookup for s in suits]

    def shuffle(self):
        if len(self.cards) > 0:
            random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 0:
            return self.cards.pop(0)


class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def display(self, n):
        print("Player", n, "cards:", end=" ")
        for card in self.cards:
            print(card, end=" ")
        print()

    def get_cards(self):
        return self.cards


class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = [Hand() for _ in range(max_players)]

    def initialize(self):

        while True:
            self.deck.shuffle()

            for n in range(max_players):
                for _ in range(4):
                    self.player[n].add_card(self.deck.deal())

            break

    def show_cards(self):
        for n in range(max_players):
            self.player[n].display(n + 1)

    def get_player(self, n):
        return self.player[n]


def list_to_string(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += str(ele)
        str1 += " "

        # return string
    return str1


server = "192.168.0.48"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(max_players)
print("Server Started, Waiting for connection")
g = Game()
g.initialize()


def threaded_client(conn, player):
    conn.send(str.encode(list_to_string(g.get_player(player).get_cards())))
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Player", player+1, "disconnected")
                break

            conn.sendall(str.encode(reply))
        except:
            break

    conn.close()


current_player = 0
while True:
    conn, addr = s.accept()
    print("Player", current_player+1, "connected to:", addr)

    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1

    if current_player == max_players:
        print("All players are connected, Initializing Game")
        g.show_cards()
    else:
        print("Waiting for other players to connect")