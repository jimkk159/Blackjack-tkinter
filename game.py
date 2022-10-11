import card
from math import floor
from player import Hand, Players
from card import Card, Deck


class Blackjack:

    def __init__(self):

        self.game_end = True

        # Setting Rule
        self.is_insurance = True
        self.is_insurance_over_10 = False
        self.is_double = True
        self.blackjack_ratio = 1.5

        # Setting Deck
        self.deck_num = 4
        self.deck = Deck(self.deck_num)
        self.deck.shuffle()

        # Setting Player
        self.player_num = 2
        self.players = None

        # Setting Banker
        self.banker = []
        self.min_bet = 5

        # Leave game player
        self.leave_man = 0

    def start(self):

        # while self.game_end:
        # self.game_reset()
        # self.banker = [Card(symbol='K', suit='spade'),
        #                Card(symbol='A', suit='heart')]
        # self.players.in_[0].hands[0].cards = [Card(symbol='A', suit='spade'),
        #                                       Card(symbol='A', suit='heart')]
        self.deal_to_all()
        # self.print_banker()
        # self.players.print_all_status()
        # if self.is_insurance:
        #     self.ask_insurance()
        # self.check_blackjack()
        # self.players.leave_game()
        # self.leave_and_money()
        # self.players.print_all_result()
        #
        # self.choice()
        # self.players.leave_game()
        # self.leave_and_money()
        #
        # self.banker_time()
        # if not self.check_bust(self.banker):
        #     self.compare_cards()
        #     self.players.leave_game()
        #     self.leave_and_money()
        #
        # self.print_banker()
        # self.players.print_all_status(choice="out")
        # print()
        # self.players.print_all_result()
        # print(self.check_sum_switch_ace(self.players.out[0].hands[0].cards))
        # print("*" * 20)
        # if input("Continue?") == "n":
        #     self.game_end = False

    # Game Setting
    def reset(self):

        if self.deck.check_deck_num():
            self.deck.reset_deck()

        # Reset Player
        # self.player_num = int(input("How many players want to participate?"))
        self.players = Players(self.player_num)
        self.players.reset_all(self.min_bet)

        # Reset Banker Cards
        self.banker = []

        # Nobody leave
        self.leave_man = 0

    # Deal Card
    def deal(self, cards_in_hand: list, faced=True):
        card = self.deck.deck.pop()
        card.faced = faced
        cards_in_hand.append(card)

    def deal_to_all(self):

        # To each player
        for player in self.players.in_:
            self.deal(player.hands[0].cards)

        # To banker
        self.deal(self.banker, faced=False)

        # To each player
        for player in self.players.in_:
            self.deal(player.hands[0].cards)

        # To banker
        self.deal(self.banker)

    # Game Start
    def ask_insurance(self):

        if self.banker[1].symbol == "A" or (
                self.is_insurance_over_10 and self.banker[1].symbol in card.poker_symbol[:5]):

            for player in self.players.in_:
                if player.money >= floor(player.stake / 2):
                    choice = input("Want to buy an insurance?")
                    if choice == "y":
                        player.money -= floor(player.stake / 2)
                        player.insurance_item = True

    # Check Sum
    def check_sum(self, cards_in_hand):

        total = 0
        for card in cards_in_hand:
            total += card.value
        return total

    def switch_ace_value(self, cards_in_hand):

        for card in cards_in_hand:
            if card.symbol == "A" and card.value == 11:
                card.value = 1
                return True
        return False

    def check_sum_switch_ace(self, cards_in_hand):

        if self.check_sum(cards_in_hand) > 21:
            self.switch_ace_value(cards_in_hand)

        return self.check_sum(cards_in_hand)

    # Check Bust
    def check_bust(self, cards_in_hand):

        if self.check_sum_switch_ace(cards_in_hand) > 21:
            return True
        return False

    # Check blackjack
    def check_cards_blackjack(self, cards_in_hand):

        if len(cards_in_hand) == 2 and self.check_sum(cards_in_hand) == 21:
            return True
        return False

    def check_blackjack(self):

        for player in self.players.in_:
            if self.check_cards_blackjack(self.banker):

                if self.check_cards_blackjack(player.hands[0].cards):
                    player.hands[0].result = "push"
                else:
                    player.hands[0].result = "lose"

            elif self.check_cards_blackjack(player.hands[0].cards):
                player.hands[0].result = "blackjack"

    # It's Player Round
    def choice(self):

        for player in self.players.in_:
            choice = input("Fold?")
            if choice == 'y':
                self.fold(player)

        for player in self.players.in_:
            self.player_choice(player)
        self.players.leave_game()
        self.leave_and_money()

    def fold(self, player):

        player.fold = True
        player.hands[0].result = "fold"

    def player_choice(self, player):

        if not player.fold:

            print()
            choice = input(f"Player {player.id} choice?")
            if choice == "double" and len(
                    player.hands[0].cards) == 2 and player.money >= player.stake and self.is_double:

                self.double_down(player)
                if self.check_bust(player.hands[0].cards):
                    print("bust")
                    player.hands[0].result = "lose"
            else:

                hand_count = 0
                while True:

                    # print("-----------------------------")
                    # print("hand_count", hand_count, len(player.hands))

                    if hand_count >= len(player.hands):
                        print("break")
                        break

                    while True:

                        if choice == "split" \
                                and len(player.hands[hand_count].cards) == 2 \
                                and player.hands[hand_count].cards[0].symbol == player.hands[hand_count].cards[1].symbol \
                                and player.money >= player.stake:
                            player.money -= player.stake
                            split_hand = Hand()
                            split_hand.cards.append(player.hands[hand_count].cards.pop())

                            player.hands[hand_count].is_ace_split = True
                            split_hand.is_ace_split = True

                            player.hands.append(split_hand)

                        if choice == "stand":
                            choice = ""
                            break

                        if choice == "hit":
                            self.hit(player.hands[hand_count])
                            if player.hands[hand_count].is_ace_split:
                                choice = ""
                                break

                        print()
                        self.players.print_all_status()
                        print("Bust?", hand_count, self.check_bust(player.hands[hand_count].cards))
                        if self.check_bust(player.hands[hand_count].cards):
                            print("This hand is bust")
                            choice = ""
                            player.hands[hand_count].result = "lose"
                            break
                        choice = input(f"Player {player.id} Hand {hand_count} choice?")

                    hand_count += 1
        # print("-----------------------------")
        # print("This is outside")
        # print("-----------------------------")

    def double_down(self, player):

        player.double = True
        player.money -= player.stake
        self.deal(player.hands[0].cards)

    def hit(self, hand):

        self.deal(hand.cards)
        if len(hand.cards) >= 5:
            hand._5_card_charlie = True

    # It's banker time
    def banker_time(self):

        while self.check_sum_switch_ace(self.banker) < 17:
            self.deal(self.banker)
            self.banker_bust()

    def banker_bust(self):

        if self.check_bust(self.banker):
            for player in self.players.in_:
                for hand in player.hands:
                    if hand.result == "":
                        hand.result = "win"

            self.players.leave_game()
            self.leave_and_money()
            return True
        return False

    # Compare the card score in hand
    def compare_cards(self):

        banker_point = self.check_sum_switch_ace(self.banker)
        for player in self.players.in_:
            for hand in player.hands:
                if hand.result == "":

                    if hand._5_card_charlie:
                        hand.result = "win"
                    else:
                        player_point = self.check_sum_switch_ace(hand.cards)
                        if player_point > banker_point:
                            hand.result = "win"
                        elif player_point < banker_point:
                            hand.result = "lose"
                        else:
                            hand.result = "push"

    # Exchange the money
    def give_money(self, player):

        for hand in player.hands:
            self.give_hand_money(hand, player)

        if player.fold:
            player.money += floor(player.stake / 2)

        if self.check_sum_switch_ace(self.banker) == 21 and player.insurance_item:
            player.money += 2 * floor(player.stake / 2)

    def give_hand_money(self, hand, player):

        if hand.result == "win":

            if hand._5_card_charlie or player.double:

                player.money += 4 * player.stake

            else:
                player.money += 2 * player.stake

        if hand.result == "blackjack":

            if player.double:
                player.money += 2 * (1 + self.blackjack_ratio) * player.stake

            elif hand._5_card_charlie:
                player.money += floor((1 + 3 * self.blackjack_ratio) * player.stake)

            else:
                player.money += floor((1 + self.blackjack_ratio) * player.stake)

        if hand.result == "push":
            if player.double:
                player.money += 2 * player.stake
            else:
                player.money += player.stake

    def leave_and_money(self):

        leaving_player = len(self.players.out)
        while self.leave_man != leaving_player:
            self.give_money(self.players.out[self.leave_man])
            self.leave_man += 1

    def print_banker(self):

        print("Banker has: ")
        print("cards: ", end="")
        for card in self.banker:
            print(f"{card.symbol} {card.suit} ", end="")
        print(f"{self.check_sum_switch_ace(self.banker)} ")
        print()

    def get_deck_num(self):
        return self.deck_num

    def get_player_num(self):
        return self.player_num

    def get_min_bet(self):
        return self.min_bet

    def get_is_insurance(self):
        return self.is_insurance

    def get_insurance_over_10(self):
        return self.is_insurance_over_10

    def get_is_double(self):
        return self.is_double

    def get_blackjack_ratio(self):
        return self.blackjack_ratio

    def set_deck_num(self, deck_num):
        self.deck_num = deck_num

    def set_player_num(self, player_num):
        self.player_num = player_num

    def set_min_bet(self, min_bet):
        self.min_bet = min_bet

    def set_is_insurance(self, is_insurance):
        self.is_insurance = is_insurance

    def set_insurance_over_10(self, is_insurance_over_10):
        self.is_insurance_over_10 = is_insurance_over_10

    def set_is_double(self, is_double):
        self.is_double = is_double

    def set_blackjack_ratio(self, blackjack_ratio):
        self.blackjack_ratio = blackjack_ratio

    def get_banker_cards(self):
        return self.banker

    def get_player_cards(self):
        return self.players.get_all_hands()

    def get_player(self):
        return self.players.get_all_players()
