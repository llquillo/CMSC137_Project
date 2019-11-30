from _thread import start_new_thread
from player import Player
import random
import socket
import pickle
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


server = "192.168.100.11"
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
players = [Player(i+1) for i in range(max_players)]
for n in range(max_players):
    for _ in range(4):
        players[n].add_card(deck.deal())

count_pass = 0
n = 0


def show_all_cards():
    for p_no in range(max_players):
        players[p_no].show_cards()


def signal_pass():
    global n
    n = 0
    while n < 3:
        n += 1
        print(n, end=" ")
        time.sleep(1)
    print("Pass!")
    time.sleep(1)


def threaded_client(conn, p_no):
    global count_pass
    conn.send(pickle.dumps(players[p_no]))
    while True:
        try:
            data = pickle.loads(conn.recv(2048))

            if not data:
                print("Player", p_no + 1, "disconnected")
                break
            else:
                card_no = int(data)

                passed_card = players[p_no].pass_card(card_no)
                print("Player", p_no + 1, "passed", passed_card)
                if p_no < max_players - 1:
                    print("Player", p_no + 2, "will received", passed_card)
                    players[p_no+1].add_card(passed_card)
                else:
                    print("Player 1 will received", passed_card)
                    players[0].add_card(passed_card)
                count_pass += 1

            if count_pass == max_players:
                signal_pass()
                show_all_cards()
                for p_no in range(max_players):
                    if players[p_no].win():
                        print("Player", p_no + 1, "win!")
                        break
                count_pass = 0
            else:
                print("Waiting for other players to pick a card")
            conn.sendall(pickle.dumps(players[p_no]))
        except:
            break

    conn.close()


current_player = 0
while True:
    conn, addr = s.accept()
    print("Player", current_player + 1, "connected to:", addr)

    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1

    if current_player == max_players:
        print("All players are connected, Initializing Game")
        show_all_cards()
    else:
        print("Waiting for other players to connect")
