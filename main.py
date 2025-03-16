import numpy as np
from utils import deal_card, get_card_representation, print_cards_horizontally, best_two_hands

"""
make card representations for a standard 52 card deck 
card number and suit
[ number, suit ]
number = 1 - 13
suit = 0,1,2,3
"""


class Player():
    def __init__(self, balance, name):
        self.balance = balance
        self.name = name
        self.is_active = True

    def add_cards(self, cards):
        self.cards = cards

    def bet(self, amt):
        if amt <= self.balance:
            self.balance -= amt
            return amt
        else:
            return "Balance Less"

    def fold(self):
        self.is_active = False


class PokerGame():
    def __init__(self, players):
        self.players = players
        self.current_pot = 0
        self.small_blind = 5
        self.big_blind = 10
        self.current_bet = self.big_blind
        self.current_cards = set()
        self.flop, self.current_cards = deal_card(self.current_cards, 3)
        self.turn, self.current_cards = deal_card(self.current_cards, 1)
        self.river, self.current_cards = deal_card(self.current_cards, 1)
        for player in self.players:
            cards, self.current_cards = deal_card(self.current_cards, 2)
            player.add_cards(cards)

    def betting_round(self):
        players_bet = {p: 0 for p in self.players if p.is_active}

        print("Small Blind: " + self.players[0].name)
        print("Big Blind: " + self.players[1].name)

        # Posting blinds
        sb_player = self.players[0]
        bb_player = self.players[1]
        sb_player.bet(self.small_blind)
        bb_player.bet(self.big_blind)
        players_bet[sb_player] = self.small_blind
        players_bet[bb_player] = self.big_blind
        self.current_pot += self.small_blind + self.big_blind

        current_bettor_index = 0  # First player to act (Under the Gun)

        while True:
            active_players = [p for p in self.players if p.is_active]
            if len(active_players) <= 1:
                break

            all_called = True
            for i in range(current_bettor_index, len(self.players)):
                player = self.players[i]
                if not player.is_active:
                    continue

                print(f"{player.name}'s turn. Current bet: {self.current_bet}")
                print_cards_horizontally(player.cards)
                action = input(
                    f"{player.name}, do you want to call (c), raise (r), or fold (f)? ")

                if action == 'c':
                    call_amount = self.current_bet - players_bet[player]
                    self.current_pot += player.bet(call_amount)
                    players_bet[player] = self.current_bet

                elif action == 'r':
                    raise_amount = int(input("Enter raise amount: "))
                    while raise_amount < self.current_bet * 2:
                        print("Raise must be at least double the current bet.")
                        raise_amount = int(input("Enter raise amount: "))

                    self.current_pot += player.bet(raise_amount -
                                                   players_bet[player])
                    self.current_bet = raise_amount
                    players_bet[player] = raise_amount
                    all_called = False

                elif action == 'f':
                    players_bet[player] = -1
                    player.fold()
                    print(f"{player.name} folds.")

                print(f"{player.name} balance: {player.balance}")
                if all(players_bet[player] == self.current_bet or players_bet[player] == -1 for player in self.players):
                    break
            if all(p.balance == 0 or not p.is_active for p in self.players) or all_called or all(players_bet[player] == self.current_bet or players_bet[player] == -1 for player in self.players):
                break
        print("Betting round complete.")


player1 = Player(1000, "Player 1")
player2 = Player(1000, "Player 2")
player3 = Player(1000, "Player 3")
game = PokerGame([player1, player2, player3])

print("Pre Flop Betting")
game.betting_round()
print("Flop")
print_cards_horizontally(game.flop)
game.betting_round()
print("Turn")
print_cards_horizontally(game.flop + game.turn)
game.betting_round()
print("River")
print_cards_horizontally(game.flop + game.turn + game.river)
game.betting_round()

best_hand, second_best_hand = best_two_hands(
    [player1.cards, player2.cards, player3.cards], game.flop + game.turn + game.river)
# print(best_hand)
print_cards_horizontally(best_hand)
