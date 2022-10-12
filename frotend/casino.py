from tkinter import *
from PIL import Image, ImageTk

import welcome
from card import Card

CHOICE_FONT = ("Arial", 10, "bold")
PLAYER_STATE_FONT = ("Arial", 24, "bold")

IMG_LEFT_BOUND = 10
IMG_UP_BOUND = 10
IMG_HORIZONTAL_SPACE = 63
IMG_VERTICAL_SPACE = 94
IMG_HORIZONTAL_INTERVAL = 2
IMG_VERTICAL_INTERVAL = 2

CARD_HORIZONTAL_MODIFY = -10


class Casino:

    def __init__(self, game, window, canvas, window_width, window_height, padding):

        # Game instance
        self.game = game

        # Game reset
        self.game.reset_player()
        self.game.reset()

        # Game Attribute
        self.deck_num = self.game.get_deck_num()
        self.player_num = self.game.get_player_num()
        self.min_bet = self.game.get_min_bet()
        self.is_ask_insurance = self.game.get_is_insurance()
        self.is_over_ten = self.game.get_insurance_over_10()
        self.is_double = self.game.get_is_double()
        self.blackjack_ratio = self.game.get_blackjack_ratio()
        self.players = self.game.get_players()

        # Interface Attribute
        self.window = window
        self.window_width = window_width
        self.window_height = window_height
        self.padding = padding
        self.table_canvas = canvas

        # Game Attribute
        self.img_suit_dict = {"heart": 0, "club": 1, "diamond": 2, "spade": 3}
        self.img_symbol_dict = {"faced": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7, "9": 8, "10": 9,
                                "J": 10, "Q": 11, "K": 12, "A": 13}
        self.game_choice_dict = {"insurance": {"yes": 0, "no": 1},
                                 "choice": {"double": 0, "split": 1, "hit": 2, "stand": 4},
                                 "end": {"continue": 0, "quit": 1}}
        self.game_state = "start"
        self.game_choice = None

        self.is_insurance = None

        self.insurance_area = None
        self.insurance_question = None
        self.insurance_choice_yes = None
        self.insurance_choice_no = None

        self.game_end_question = None
        self.game_end_area = None
        self.game_end_continue = None
        self.game_end_quit = None

        self.player_choice_question = None
        self.player_choice_area = None
        self.player_option_result = None
        self.player_choice_double = None
        self.player_choice_split = None
        self.player_choice_hit = None
        self.player_choice_stand = None

        self.banker_img = []
        self.players_img = []

        # Table Image
        table_img = Image.open("../img/pixel-blackjack_big.png")
        table_img = table_img.resize((800, 400))
        self.table_canvas.table_pic = ImageTk.PhotoImage(table_img)
        self.table_canvas.create_image(400, 200, image=self.table_canvas.table_pic)

        # Card Image
        card_img_map = Image.open("../img/poker_card.png")

        card_img_map = card_img_map.resize((1000, 400))
        card_img_map_x = [(10, 73), (74, 137), (138, 201), (203, 266), (267, 330), (332, 394), (396, 458), (460, 523),
                          (524, 587), (589, 652), (653, 716), (718, 780), (782, 845), (846, 909)]
        card_img_map_y = [(11, 104), (106, 200), (202, 294), (296, 389)]
        self.card_coordinates = [(x[0], y[0], x[1], y[1]) for y in card_img_map_y for x in card_img_map_x]

        self.table_canvas.cards = []
        for num in range(len(self.card_coordinates)):
            card_coordinate = self.card_coordinates[num]
            slice_img = card_img_map.crop(card_coordinate)
            self.table_canvas.card = ImageTk.PhotoImage(slice_img)
            self.table_canvas.cards.append(ImageTk.PhotoImage(slice_img))

        # Banker Area
        banker_area = self.table_canvas.create_rectangle(325, 30, 475, 130, outline="black", width=3)

        # Player Area
        self.players_area = []
        self.players_area_xy = []
        if self.player_num == 1:
            self.players_area.append(self.table_canvas.create_rectangle(350, 260, 450, 340, outline="black", width=3))
            self.players_area_xy.append((350, 260, 450, 340))
        elif self.player_num == 2:
            self.players_area.append(self.table_canvas.create_rectangle(150, 230, 250, 310, outline="black", width=3))
            self.players_area.append(self.table_canvas.create_rectangle(550, 230, 650, 310, outline="black", width=3))
            self.players_area_xy.append((150, 230, 250, 310))
            self.players_area_xy.append((550, 230, 650, 310))
        elif self.player_num == 3:
            self.players_area.append(self.table_canvas.create_rectangle(120, 230, 220, 310, outline="black", width=3))
            self.players_area.append(self.table_canvas.create_rectangle(350, 260, 450, 340, outline="black", width=3))
            self.players_area.append(self.table_canvas.create_rectangle(580, 230, 680, 310, outline="black", width=3))
            self.players_area_xy.append((120, 230, 220, 310))
            self.players_area_xy.append((350, 260, 450, 340))
            self.players_area_xy.append((580, 230, 680, 310))
        self.money = self.table_canvas.create_text(10, 10, text=f"Money: {self.game.get_players()[0].money}",
                                                   font=PLAYER_STATE_FONT, anchor="nw", fill="black")
        self.stake = self.table_canvas.create_text(10, 50, text=f"Stake: {self.game.get_players()[0].basic_stake}",
                                                   font=PLAYER_STATE_FONT, anchor="nw", fill="black")
        self.control_casino()
        self.game_start()

    def game_start(self):

        # Game start
        self.game.reset()
        self.game.deal_to_all()
        # self.game.banker = [Card(symbol='K', suit='spade', faced=False),
        #                     Card(symbol='A', suit='heart')]
        self.game.get_players()[0].hands[0].cards = [Card(symbol='A', suit='spade'),
                                                     Card(symbol='A', suit='heart')]
        self.game_state = "insurance"
        self.show_banker_card()
        self.show_players_card()
        self.update_money(self.game.get_players()[0])
        self.update_stake(self.game.get_players()[0])
        if self.is_ask_insurance:
            self.ask_insurance()
        else:
            self.game_state = "choice"
            self.player_choice()

    # Check Blackjack
    def check_blackjack(self):
        if self.game.check_cards_blackjack(self.game.banker):
            self.game.banker[0].faced = True
            self.show_banker_card()
        game_end = self.game.check_blackjack()
        self.check_player_end()
        if game_end:
            self.update_money(self.game.get_players()[0])
            self.update_stake(self.game.get_players()[0])
        self.game.players.leave_game()
        self.game.leave_and_money()
        if not game_end:
            self.game_state = "choice"
            self.player_choice()

    # Ask Insurance
    def ask_insurance(self):

        if self.game.get_judge_insurance():
            self.game_state = "insurance"
            self.game_choice = self.game_choice_dict["insurance"]["yes"]
            self.is_insurance = True
            # for num in range(self.player_num):
            x1, y1, x2, y2 = self.players_area_xy[0]
            result = self.show_question(x1 - 130, y1, question="Buy insurance?", options=["Yes", "No"])
            [frame, self.insurance_area, self.insurance_question,
             [self.insurance_choice_yes, self.insurance_choice_no]] = result
        else:
            self.game_state = "choice"
            self.player_choice()

    # Player Choice
    def player_choice(self):
        self.game_choice = self.game_choice_dict["choice"]["double"]
        x1, y1, x2, y2 = self.players_area_xy[0]
        q_config = {"font": ("Arial", 14, "bold")}
        player_option_dict = {"double": ["Double down", self.player_choice_double],
                              "split": ["Split", self.player_choice_split],
                              "hit": ["Hit", self.player_choice_hit],
                              "stand": ["Stand", self.player_choice_stand]}
        player_option = []
        for option in self.game.get_player_option(self.game.get_players()[0], self.game.get_players()[0].hands[0]):
            player_option.append(player_option_dict[option][0])
        result = self.show_question(x1 - 145, y1 - 15, question="Your Choice:", q_config=q_config,
                                    options=player_option)
        [frame, self.player_choice_area, self.player_choice_question,
         self.player_option_result] = result

    # Show Question Area
    def show_question(self, x, y, question=None, q_config=None, options=None, o_config=None):

        frame = Frame(self.window, bg="black")
        frame.grid()

        row = 0
        if question:
            question = Label(frame, text=question, fg="white", bg="black", font=CHOICE_FONT)
            if q_config:
                question.config(q_config)
            question.grid(column=0, row=row)
            row += 1

        options_array = []
        for num in range(len(options)):
            if num == 0:
                option = Label(frame, text=options[num], fg="black", bg="white", font=CHOICE_FONT)
            else:
                option = Label(frame, text=options[num], fg="white", bg="black", font=CHOICE_FONT)
            if o_config and o_config[num]:
                option.config(o_config[num])
            option.grid(column=0, row=row)
            options_array.append(option)
            row += 1
        area = self.table_canvas.create_window(x, y, window=frame, anchor="nw")
        return [frame, area, question, options_array]

    # Check Player State
    def check_player_end(self):

        # TODO only check player 1 now
        hands = self.game.get_players()[0].hands
        game_result = all([(True if hand.result != "" else False) for hand in hands])
        if game_result:
            self.game_state = "game end"
            self.game_choice = self.game_choice_dict["end"]["continue"]
            self.show_game_end()

    # Show Game End
    def show_hand_result(self):

        game_result = ""
        # TODO only check player 1 now
        hands = self.game.get_players()[0].hands
        for num in range(len(hands)):
            if num != 0:
                game_result += " "
            if hands[num].result == "push":
                game_result += "PUSH"
            elif hands[num].result == "blackjack":
                game_result += "BlackJack"
            elif hands[num].result == "lose":
                game_result += "LOSE"
            elif hands[num].result == "win":
                game_result += "WIN"
        return game_result

    def show_game_end(self):
        q_config = {"font": ("Arial", 30, "bold")}
        o_config = [{"font": ("Arial", 18, "bold")}, {"font": ("Arial", 18, "bold")}]
        game_result = self.show_hand_result()
        result = self.show_question(300, 150, question=f"Result: {game_result}\n"
                                                       f"Game End", q_config=q_config,
                                    options=["Continue", "Quit"],
                                    o_config=o_config)
        [frame, self.game_end_area, self.game_end_question, [self.game_end_continue, self.game_end_quit]] = result

    # Show Card
    def show_card(self, x, y, card_loc, faced):

        if faced:
            return self.table_canvas.create_image(x, y, image=self.table_canvas.cards[card_loc], anchor="nw")
        else:
            return self.table_canvas.create_image(x, y, image=self.table_canvas.cards[0], anchor="nw")

    def show_banker_card(self):

        # Delete the previous card img
        if not self.banker_img:
            self.delete_imgs(self.banker_img)
            self.banker_img = []

        # Create card img
        cards = self.game.banker
        for card_num in range(len(cards)):
            card = cards[card_num]
            card_loc = 14 * self.img_suit_dict[card.suit] + self.img_symbol_dict[card.symbol]
            self.banker_img.append(
                self.show_card(325 + 68 * card_num + CARD_HORIZONTAL_MODIFY, 30, card_loc, card.faced))

    def show_players_card(self):

        # Create card img
        for player_num in range(self.player_num):
            self.show_player_card(player_num,
                                  self.players_area_xy[player_num][0],
                                  self.players_area_xy[player_num][1])

    def show_player_card(self, player_num, x, y):

        # Delete the previous card img
        if not self.players_img:
            if len(self.players_img) > player_num:
                for cards_img in self.players_img[player_num]:
                    self.delete_imgs(cards_img)
                self.players_img[player_num] = []

        # Create a list to save specific player img
        while len(self.players_img) <= player_num:
            self.players_img.append([])

        hands = self.players[player_num].get_hands()

        # Player split card has multiple hands
        for _ in range(len(hands)):
            self.players_img[player_num].append([])

        # Create card im
        for hand_num in range(len(hands)):
            hand = hands[hand_num]
            cards = hand.cards
            for card_num in range(len(cards)):
                card = cards[card_num]
                card_loc = 14 * self.img_suit_dict[card.suit] + self.img_symbol_dict[card.symbol]
                card_img = self.show_card(x + 68 * card_num + CARD_HORIZONTAL_MODIFY, y, card_loc, card.faced)
                self.players_img[player_num][hand_num].append(card_img)

    def delete_imgs(self, imgs):
        for img in imgs:
            self.table_canvas.delete(img)

    # Update Money
    def update_money(self, player):
        self.table_canvas.itemconfig(self.money, text=f"Money: {player.money}")

    def update_stake(self, player):
        self.table_canvas.itemconfig(self.stake, text=f"Stake: {player.total_stake}")

    # Control Table
    def control_casino(self):
        self.window.bind('<Up>', self.upKey)
        self.window.bind('<Down>', self.downKey)
        self.window.bind('<Left>', self.leftKey)
        self.window.bind('<Right>', self.rightKey)
        self.window.bind('<Return>', self.enterKey)

    def switch_choice(self, pre_choice, move, choices):

        now_choice = pre_choice
        if move == "up" and pre_choice > 0:
            now_choice = pre_choice - 1
        elif move == "down" and pre_choice < len(choices) - 1:
            now_choice = pre_choice + 1
        choices[pre_choice].config(fg="white", bg="black")
        choices[now_choice].config(fg="black", bg="white")
        return now_choice

    # Keyboard
    def upKey(self, event):
        if self.game_state == "insurance":
            self.is_insurance = True
            choice_list = [self.insurance_choice_yes, self.insurance_choice_no]
            self.game_choice = self.switch_choice(self.game_choice, "up", choice_list)
        elif self.game_state == "choice":
            choice_list = self.player_option_result
            self.game_choice = self.switch_choice(self.game_choice, "up", choice_list)
        elif self.game_state == "game end":
            choice_list = [self.game_end_continue, self.game_end_quit]
            self.game_choice = self.switch_choice(self.game_choice, "up", choice_list)
        print("Up key pressed")

    def downKey(self, event):
        if self.game_state == "insurance":
            self.is_insurance = False
            choice_list = [self.insurance_choice_yes, self.insurance_choice_no]
            self.game_choice = self.switch_choice(self.game_choice, "down", choice_list)
        elif self.game_state == "choice":
            choice_list = self.player_option_result
            self.game_choice = self.switch_choice(self.game_choice, "down", choice_list)
        elif self.game_state == "game end":
            choice_list = [self.game_end_continue, self.game_end_quit]
            self.game_choice = self.switch_choice(self.game_choice, "down", choice_list)
        print("Down key pressed")

    def leftKey(self, event):
        print("Left key pressed")

    def rightKey(self, event):
        print("Right key pressed")

    def enterKey(self, event):
        if self.game_state == "insurance":
            self.game.ask_insurance(self.is_insurance)
            self.table_canvas.delete(self.insurance_area)
            self.game_state = "blackjack"
            self.check_blackjack()
        elif self.game_state == "choice":
            if self.game_choice == self.game_choice_dict["choice"]["double"]:
                self.game.double_down_process(self.game.get_players()[0])
                self.update_money(self.game.get_players()[0])
                self.update_stake(self.game.get_players()[0])
                self.show_players_card()
                self.check_player_end()
            elif self.game_choice == self.game_choice_dict["choice"]["split"]:
                pass
            elif self.game_choice == self.game_choice_dict["choice"]["hit"]:
                pass
            elif self.game_choice == self.game_choice_dict["choice"]["stand"]:
                pass
        elif self.game_state == "game end":
            if self.game_choice == self.game_choice_dict["end"]["continue"]:
                self.game_start()
                self.table_canvas.delete(self.game_end_area)
            elif self.game_choice == self.game_choice_dict["end"]["quit"]:
                self.table_canvas.delete("all")
                welcome_ = welcome.Welcome(self.game, self.window, self.table_canvas, self.window_width,
                                           self.window_height, self.padding)
                del self
        print("Enter key pressed")
