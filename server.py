from _thread import start_new_thread
import random
import socket
import pickle
import time

address = input("Enter IPv4 address: ")
n_players = int(input("Enter number of players [3-13]: "))

suits = ['C', 'D', 'H', 'S']
ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']

rank_lookup = {}
for i in range(n_players):
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


class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.cards = []

    def add_card(self, card):
        return self.cards.append(str(card))

    def pass_card(self, card_no):
        return self.cards.pop(card_no)

    def show_cards(self):
        print("Player", self.player_id + 1, "cards:", end=" ")
        for card in self.cards:
            print(card, end=" ")
        print()

    def win(self):
        return all(str(x)[0] == str(self.cards[0])[0] for x in self.cards)


class Game:
    def __init__(self, max_players):
        self.deck = Deck()
        self.max_players = max_players
        self.players = [Player(p_no) for p_no in range(self.max_players)]
        self.pass_count = 0
        self.winner = -1
        self.table_count = 0

    def initialize(self):
        self.deck.shuffle()

        for p_no in range(self.max_players):
            for _ in range(4):
                self.players[p_no].add_card(self.deck.deal())

    def show_all_cards(self):
        for p_no in range(self.max_players):
            self.players[p_no].show_cards()

    def set_winner(self, player):
        self.winner = player


server = address
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(n_players)
print("Server Started, Waiting for connection")
g = Game(n_players)
g.initialize()


def signal_pass():
    c = 0
    while c < 3:
        c += 1
        print(c, end=" ")
        time.sleep(1)
    print("Pass!")
    time.sleep(1)


def threaded_client(conn, p_no):
    conn.send(pickle.dumps([g.players[p_no].player_id, g.players[p_no].cards]))
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            player = [g.players[p_no].player_id, g.players[p_no].cards, g.pass_count, g.max_players, g.winner]

            if not data:
                print("Player", g.players[p_no].player_id + 1, "put his/her hand on the table!")
                g.table_count += 1
            elif data == "wait":
                print("Waiting for other players to pick a card")
                g.pass_count += 1
                time.sleep(5)
            elif data == "pass":
                signal_pass()
                g.show_all_cards()
                g.pass_count = 0
                print("End of turn, Waiting for players to pick a card")
            elif data == "win":
                for p in range(g.max_players):
                    if g.players[p].win():
                        g.winner = p
                player = [p_no, g.players[p_no].cards, g.pass_count, g.max_players, g.winner]
            else:
                card_no = int(data)
                passed_card = g.players[p_no].pass_card(card_no)
                print("Player", p_no + 1, "picked", passed_card)
                if p_no < g.max_players - 1:
                    print("Player", p_no + 2, "will received", passed_card)
                    g.players[p_no + 1].add_card(passed_card)
                else:
                    print("Player 1 will received", passed_card)
                    g.players[0].add_card(passed_card)

            if g.winner >= 0 and g.table_count == g.max_players:
                print("Player", g.winner + 1, "wins!")
                print("Player", g.players[p_no].player_id + 1, "lose!")
                print("End game, Restart server and client to play again")
            conn.sendall(pickle.dumps(player))

        except:
            break

    conn.close()


current_player = 0
while True:
    conn, addr = s.accept()
    print("Player", current_player + 1, "connected to:", addr)

    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1

    if current_player == g.max_players:
        print("All players are connected, Initializing Game")
        g.show_all_cards()
        print("Waiting for players to pick a card")
    else:
        print("Waiting for other players to connect")
