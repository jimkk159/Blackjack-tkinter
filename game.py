from math import floor
from player import Hand, Players
from card import Deck


class Blackjack:

    def __init__(self):

        self.game_end = False

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

    # GET
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

    def get_player_can_double(self, player):
        if len(player.get_hands()[0].get_cards()) == 2 and \
                player.get_money() >= player.get_basic_stake() and \
                self.is_double and player.get_hands_num() == 1:
            return True
        return False

    def get_hand_can_split(self, player, hand):
        if len(hand.get_cards()) == 2 and \
                hand.get_cards()[0].get_symbol() == hand.get_cards()[1].get_symbol() \
                and player.get_money() >= player.get_basic_stake():
            return True
        return False

    def get_judge_insurance(self):
        if self.banker[1].get_symbol() == "A" or (
                self.is_insurance_over_10 and self.banker[1].get_symbol() in ["A", "K", "Q", "J", "10"]):
            return True
        return False

    def get_is_double(self):
        return self.is_double

    def get_blackjack_ratio(self):
        return self.blackjack_ratio

    def get_banker_cards(self):
        return self.banker

    def get_player_cards(self):
        return self.players.get_all_hands()

    def get_players(self):
        return self.players

    def get_players_in(self):
        return self.players.get_players_in()

    def get_player_option(self, player, hand):
        result = []
        if self.get_player_can_double(player):
            result.append("double")
        if self.get_hand_can_split(player, hand):
            result.append("split")
        result += ["hit", "stand"]
        return result

    def get_player_stake(self, player):
        return player.get_total_stake()

    def get_hand_is_charlie(self, hand):
        return hand.get_is_charlie()

    # Check Bust
    def get_is_hand_bust(self, cards_in_hand):

        if self.get_hand_sum_switch_ace(cards_in_hand) > 21:
            return True
        return False

    def get_player_insurance(self, player):
        return player.get_insurance()


    # Check Sum
    def get_hand_sum(self, cards_in_hand):

        total = 0
        for card_ in cards_in_hand:
            total += card_.get_value()
        return total

    def switch_ace_value(self, cards_in_hand):

        for card_ in cards_in_hand:
            if card_.get_symbol() == "A" and card_.get_value() == 11:
                card_.set_value(1)
                return True
        return False

    def get_hand_sum_switch_ace(self, cards_in_hand):

        while self.get_hand_sum(cards_in_hand) > 21:
            if not self.switch_ace_value(cards_in_hand):
                break

        return self.get_hand_sum(cards_in_hand)

    def get_is_blackjack(self, cards_in_hand):

        if len(cards_in_hand) == 2 and self.get_hand_sum(cards_in_hand) == 21:
            return True
        return False

    def get_is_banker_bust(self):

        if self.get_is_hand_bust(self.banker):
            return True
        return False

    # SET
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

    def set_player_insurance(self, player, insurance: bool):

        player.set_insurance(insurance)

    def reset_player_insurance(self, player):

        player.set_insurance(False)

    def check_blackjack(self):

        return all(map(self.check_player_blackjack, self.get_players_in()))

    def check_player_blackjack(self, player):

        hand = player.get_hands()[0]
        banker_blackjack = self.get_is_banker_blackjack()
        player_blackjack = self.get_is_player_blackjack(player)

        if banker_blackjack and player_blackjack:
            hand.set_result("push")
            return True

        if banker_blackjack:
            hand.set_result("lose")
            return True

        if player_blackjack:
            hand.set_result("blackjack")
            return True
        return False

    def get_is_banker_blackjack(self):
        if self.get_is_blackjack(self.banker):
            return True
        return False

    def get_is_player_blackjack(self, player):
        hand = player.get_hands()[0]
        if self.get_is_blackjack(hand.get_cards()):
            return True
        return False

    # Game Setting
    def reset(self):

        if self.deck.get_cards_enough():
            self.deck.reset_deck()

        # Reset Player
        result = self.players.reset_all()

        # Reset Banker Cards
        self.banker = []

        # Nobody leave
        self.leave_man = 0

        return result

    def reset_player(self):
        self.players = Players(self.player_num)

    # Deal Card
    def deal(self, cards_in_hand: list, faced=True):
        card_ = self.deck.get_deck().pop()
        card_.faced = faced
        cards_in_hand.append(card_)

    def deal_to_all(self):

        # To each player
        for player in self.players.get_players_in():
            self.deal(player.get_hands()[0].get_cards())

        # To banker
        self.deal(self.banker, faced=False)

        # To each player
        for player in self.players.in_:
            self.deal(player.get_hands()[0].get_cards())

        # To banker
        self.deal(self.banker)

    # Ask Insurance
    def ask_insurance(self, choice):

        # ToDo only for player 1
        # for num in range(self.player_num):
        self.ask_player_insurance(self.players.get_players_in()[0], choice)

    def ask_player_insurance(self, player, choice):

        player.set_insurance(False)
        if choice and player.get_money() >= floor(player.get_basic_stake() / 2):
            player.add_money(-floor(player.get_basic_stake() / 2))
            player.set_insurance(True)

    # It's Player Round
    def choice(self):

        for player in self.players.get_players_in():
            choice = input("Fold?")
            if choice == 'y':
                self.fold(player)

        for player in self.players.get_players_in():
            self.player_choice(player)
        self.players.eliminate()
        self.give_money_all()

    def fold(self, player):

        player.set_fold(True)
        player.get_hands()[0].set_result("fold")

    def player_choice(self, player):

        if not player.fold:
            print()
            choice = input(f"Player {player.id} choice?")
            if choice == "double" and self.get_player_can_double(player):
                self.double_down_process(player)

            else:

                hand_count = 0
                while True:

                    if hand_count >= len(player.get_hands()):
                        print("break")
                        break

                    while True:

                        if choice == "split" and self.get_hand_can_split(player, player.get_hands()[hand_count]):
                            player.add_money(-player.get_basic_stake())
                            player.add_total_stake(player.get_basic_stake())
                            split_hand = Hand()
                            split_hand.get_cards().append(player.get_hands()[hand_count].get_cards().pop())

                            player.get_hands()[hand_count].set_is_ace_split(True)
                            split_hand.set_is_ace_split(True)
                            player.get_hands().append(split_hand)

                        if choice == "stand":
                            choice = ""
                            break

                        if choice == "hit":
                            self.hit(player.get_hands()[hand_count])
                            if player.get_hands()[hand_count].get_is_ace_split():
                                choice = ""
                                break

                        print()
                        self.players.print_all_status()
                        print("Bust?", hand_count, self.get_is_hand_bust(player.get_hands()[hand_count].get_cards()))
                        if self.get_is_hand_bust(player.get_hands()[hand_count].get_cards()):
                            print("This hand is bust")
                            choice = ""
                            player.get_hands()[hand_count].get_result = "lose"
                            break
                        choice = input(f"Player {player.get_id()} Hand {hand_count} choice?")

                    hand_count += 1

    # Double Down
    def double_down(self, player):

        player.set_double(True)
        player.add_money(-player.get_basic_stake())
        player.set_total_stake(2 * player.get_basic_stake())
        self.deal(player.get_hands()[0].get_cards())

    def double_down_process(self, player):
        self.double_down(player)
        if self.get_is_hand_bust(player.get_hands()[0].get_cards()):
            player.get_hands()[0].set_result("lose")

    # Hit
    def hit(self, hand):
        self.deal(hand.get_cards())
        if len(hand.cards) >= 5:
            hand.set_charlie(True)

    def hit_process(self, hand):
        self.hit(hand)
        if self.get_is_hand_bust(hand.get_cards()):
            hand.set_result("lose")

    # Split
    def split(self, hands, hand):

        # Separate the card
        split_card = hand.get_cards().pop()
        hand.set_is_ace_split(True)

        # Create New Hand
        split_hand = Hand()
        split_hand.get_cards().append(split_card)
        split_hand.set_is_ace_split(True)

        # Assign the hand to player
        hands.append(split_hand)

    def split_process(self, player, hand):

        player.add_money(-player.get_basic_stake())
        player.add_total_stake(player.get_basic_stake())
        self.split(player.get_hands(), hand)

    # It's banker time
    def reveal_banker_card(self):
        self.banker[0].set_faced(True)

    def deal_to_banker(self):

        while self.get_hand_sum_switch_ace(self.banker) < 17:
            self.deal(self.banker)

    def banker_bust_process(self):

        for player in self.players.get_players_in():
            for hand in player.get_hands():
                hand_result = hand.get_result()
                if hand_result == "" or hand_result == "stand":
                    hand.set_result("win")

    # Compare the card score in hand
    def compare_cards(self):

        banker_point = self.get_hand_sum_switch_ace(self.banker)
        for player in self.players.get_players_in():
            for hand in player.get_hands():
                hand_result = hand.get_result()
                if hand_result == "" or hand_result == "stand":

                    if hand.get_is_charlie():
                        hand.set_result("win")
                    else:
                        player_point = self.get_hand_sum_switch_ace(hand.get_cards())
                        if player_point > banker_point:
                            hand.set_result("win")
                        elif player_point < banker_point:
                            hand.set_result("lose")
                        else:
                            hand.set_result("push")

    # Exchange the money
    def give_hand_money(self, hand, player):

        if hand.get_result() == "win":

            if hand.get_is_charlie() or player.get_double():

                player.add_money(4 * player.get_basic_stake())

            else:

                player.add_money(2 * player.get_basic_stake())

        if hand.get_result() == "blackjack":

            if player.get_double():
                player.add_money(2 * (1 + self.blackjack_ratio) * player.get_basic_stake())

            elif hand.get_is_charlie():
                player.money.add_money(floor((1 + 3 * self.blackjack_ratio) * player.get_basic_stake()))

            else:
                player.add_money(floor((1 + self.blackjack_ratio) * player.get_basic_stake()))

        if hand.get_result() == "push":
            if player.get_double():
                player.add_money(2 * player.get_basic_stake())
            else:
                player.add_money(player.get_basic_stake())

    def give_money(self, player):

        for hand in player.get_hands():
            self.give_hand_money(hand, player)

        if player.get_fold():
            player.add_money(floor(player.get_basic_stake() / 2))

        if self.get_hand_sum_switch_ace(self.banker) == 21 and player.get_insurance():
            player.add_money(2 * floor(player.get_basic_stake() / 2))

    def give_money_all(self):

        leaving_player = len(self.players.get_players_out())
        while self.leave_man != leaving_player:
            self.give_money(self.players.get_players_out()[self.leave_man])
            self.leave_man += 1

    def print_banker(self):

        print("Banker has: ")
        print("cards: ", end="")
        for card_ in self.banker:
            print(f"{card_.get_symbol()} {card_.get_suit()} ", end="")
        print(f"{self.get_hand_sum_switch_ace(self.banker)} ")
        print()
