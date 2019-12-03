import socket
import pickle


class Network:
    def __init__(self, server):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player = self.connect()

    def get_player(self):
        return self.player

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)


def select_card():
    n = int(input("Select a card to pass [1-4]: "))
    return n - 1


def main():
    server = input("Enter server IPv4 address: ")
    n = Network(server)
    p = n.get_player()
    print("You are Player", p[0] + 1)

    """
    p[0]: player_id
    p[1]: player_cards
    p[2]: pass_count
    p[3]: max_no_of_players
    p[4]: winner
    """

    while True:
        print("Your cards:", *p[1])
        n.send(str(select_card()))
        print("Waiting for other players to pick a card")
        p = n.send(str("wait"))
        if p[2] + 1 == p[3]:
            n.send(str("pass"))
            p = n.send(str("win"))
            if p[4] >= 0:
                print("Player", p[4] + 1, "wins!")
                while True:
                    i = input("Press [enter] to put hand on the middle of the table: ")
                    n.send(str(i))
                    if not i:
                        break
                exit()


main()
