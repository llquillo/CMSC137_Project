from network import Network


def main():

    n = Network()
    p = n.get_player()

    while True:
        p.show_cards()
        p.pass_card()


main()
