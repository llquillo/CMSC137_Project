import time
from network import Network


def select_card():
    n = int(input("Select a card to pass [1-4]: "))
    return n - 1


def main():

    n = Network()
    p = n.get_player()
    print("You are Player", p.get_player_id())
    print("Waiting for other players to connect")
    time.sleep(10)

    while True:
        p.show_cards()
        c = select_card()
        p.pass_card(c)
        n.send(str(c))
        print("Waiting for other players to pick a card")
        time.sleep(10)


main()
