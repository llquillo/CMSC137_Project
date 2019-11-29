from _thread import start_new_thread
from player import Player
import random
import socket
import pickle


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


server = "192.168.0.48"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(max_players)
print("Server Started, Waiting for connection")

deck = Deck()
deck.shuffle()
players = [Player() for _ in range(max_players)]
for n in range(max_players):
    for _ in range(4):
        players[n].add_card(deck.deal())


def threaded_client(conn, player_no):
    conn.send(pickle.dumps(players[player_no]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player_no] = data

            if not data:
                print("Player", player_no + 1, "disconnected")
                break
            else:
                reply = players[player_no]

                print("Received: ", data)
                print("Sending :", reply)

            conn.sendall(pickle.dumps(reply))
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
        for i in range(max_players):
            players[i].show_cards()
    else:
        print("Waiting for other players to connect")
