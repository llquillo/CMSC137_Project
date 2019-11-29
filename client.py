from network import Network


def select_card():
    n = int(input("Select a card to pass [1-4]: "))
    return n - 1


def main():

    n = Network()
    p = n.get_player()
    print("You are Player", p.get_player_id())

    while True:
        p.show_cards()
        c = select_card()
        p.pass_card(c)
        n.send(str(c))


main()
