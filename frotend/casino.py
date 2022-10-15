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

IMG_HAND_CARD_SPACE = 40
IMG_HAND_CHOICE_SPACE = 60

CARD_HORIZONTAL_MODIFY = -10


class Casino:

    def __init__(self, game, window, canvas, window_width, window_height, padding):

        # Game instance
        self.game = game

        # Game reset
        self.game.reset_player()

        # Game Attribute
        self.deck_num = self.game.get_deck_num()
        self.player_num = self.game.get_player_num()
        self.min_bet = self.game.get_min_bet()
        self.is_ask_insurance = self.game.get_is_insurance()
        self.is_over_ten = self.game.get_insurance_over_10()
        self.is_double = self.game.get_is_double()
        self.blackjack_ratio = self.game.get_blackjack_ratio()
        self.players = self.game.get_players_in()

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
        self.game_interface_dict = {
            "insurance": {"frame": None, "area": None, "question": None, "result": None, "options": None},
            "choice": {"frame": None, "area": None, "question": None, "result": None, "options": None},
            "end": {"frame": None, "area": None, "question": None, "result": None, "options": None}}
        self.game_state = "start"
        self.game_choice = 0

        self.is_insurance = None
        self.now_player = self.game.get_players_in()[0]

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
        self.money = self.table_canvas.create_text(10, 10, text=f"Money: {self.now_player.get_money()}",
                                                   font=PLAYER_STATE_FONT, anchor="nw", fill="black")
        self.stake = self.table_canvas.create_text(10, 50, text=f"Stake: {self.now_player.get_basic_stake()}",
                                                   font=PLAYER_STATE_FONT, anchor="nw", fill="black")
        self.control_casino()
        self.game_start()

    def game_start(self):

        # Game start
        reset_result = self.game.reset()
        if reset_result[0]:
            self.game.deal_to_all()

            # For Debug Test
            # self.game.banker = [Card(symbol='K', suit='spade', faced=False),
            #                     Card(symbol='A', suit='heart')]
            # self.now_player.get_hands()[0].cards = [Card(symbol='A', suit='spade'),
            #                                         Card(symbol='A', suit='heart')]
            self.game_state = "insurance"
            self.show_banker_card()
            self.show_players_card()
            self.update_money(self.now_player)
            self.update_stake(self.now_player)
            if self.is_ask_insurance:
                self.ask_insurance()
            else:
                self.player_choice(self.now_player)
        else:
            self.game_state = "no money"
            self.show_game_end()

    # Check Blackjack
    def check_blackjack(self):
        if self.game.get_is_blackjack(self.game.banker):
            self.game.banker[0].faced = True
            self.show_banker_card()
        game_end = self.game.check_blackjack()
        game_end = self.is_player_end()
        if game_end:
            self.game_end_process()
        else:
            self.player_choice(self.now_player)


    # End Process
    def game_end_process(self):

        # ToDo only care player 1 win or lose now
        game_end = self.is_player_end()
        if game_end:
            self.game_state = "end"
            self.game_choice = 0
            self.show_game_end()
            self.update_money(self.now_player)
            self.update_stake(self.now_player)
        self.game.get_players().eliminate()
        self.game.give_money_all()

    # Ask Insurance
    def ask_insurance(self):

        if self.game.get_judge_insurance():
            self.game_state = "insurance"
            self.game_choice = 0
            self.is_insurance = True

            # Create Area
            # for num in range(self.player_num):
            x1, y1, x2, y2 = self.players_area_xy[0]
            result = self.show_question(x1 - 130, y1, question="Buy insurance?", options=["Yes", "No"])
            self.game_interface_dict[self.game_state] = result
        else:
            self.player_choice(self.now_player)

    # Player Choice
    def player_choice(self, player):
        hands = player.get_hands()
        for num in range(len(hands)):
            result = hands[num].get_result()
            if result == "":
                self.player_hand_choice(player, num)
                break

    # Set Player hand Hit
    def set_player_hit(self, player):
        hands = player.get_hands()
        for hand in hands:
            if hand.get_result() == "":
                self.game.hit_process(hand)
                break

    # Set Player hand Stand
    def set_player_stand(self, player):
        hands = player.get_hands()
        for hand in hands:
            if hand.get_result() == "":
                self.set_hand_stand(hand)
                break

    # Set Player Hand Result Stand
    def set_hand_stand(self, hand):
        hand.set_result("stand")

    # Player Hand Choice
    def player_hand_choice(self, player, hand_num):
        self.game_state = "choice"
        x1, y1, x2, y2 = self.players_area_xy[0]
        q_config = {"font": ("Arial", 14, "bold")}
        player_option_dict = {"double": "Double down",
                              "split": "Split",
                              "hit": "Hit",
                              "stand": "Stand"}

        # Create Area
        player_option = []

        # TODO options for player 1
        # plyer_one = self.now_player
        # plyer_one_hand = self.now_player.hands[0]

        self.game_choice = 0

        # options = self.game.get_player_option(plyer_one, plyer_one_hand)
        hand = player.get_hands()[hand_num]
        options = self.game.get_player_option(player, hand)
        for option in options:
            player_option.append(player_option_dict[option])

        result = self.show_question(x1 - 143, y1 - 15 + IMG_HAND_CHOICE_SPACE * hand_num, question="Your Choice:",
                                    q_config=q_config,
                                    options=player_option, o_index=options)
        self.game_interface_dict[self.game_state] = result

    # Show Question Area
    def show_question_block(self, frame, items, item_config, row, index=None):

        if items:

            if type(items) != list:
                item = Label(frame, text=items, fg="white", bg="black", font=CHOICE_FONT)
                if item_config:
                    item.config(item_config)
                item.grid(column=0, row=row)
                return item, row + 1
            else:
                item_dict = {}
                temp_row = row
                for num in range(len(items)):
                    if num == 0:
                        item = Label(frame, text=items[num], fg="black", bg="white", font=CHOICE_FONT)
                    else:
                        item = Label(frame, text=items[num], fg="white", bg="black", font=CHOICE_FONT)
                    if item_config and item_config[num]:
                        item.config(item_config[num])
                    item.grid(column=0, row=temp_row)
                    item_dict[num] = [item]
                    if index:
                        item_dict[num].append(index[num])
                    temp_row += 1
                return item_dict, temp_row + 1
        return items, row

    # Destroy Canvas OBJ
    def destroy_obj(self, obj):
        if obj:
            self.table_canvas.delete(obj)

    # Show Question
    def show_question(self, x, y, question=None, q_config=None, game_result=None, r_config=None
                      , options=None, o_index=None, o_config=None):

        frame = Frame(self.window, bg="black")
        frame.grid()

        row = 0
        question, row = self.show_question_block(frame, question, q_config, row)
        game_result, row = self.show_question_block(frame, game_result, r_config, row)
        options_dict, row = self.show_question_block(frame, options, o_config, row, index=o_index)
        area = self.table_canvas.create_window(x, y, window=frame, anchor="nw")

        result = {"frame": frame, "area": area}
        if question:
            result["question"] = question
        if game_result:
            result["result"] = game_result
        if options:
            result["options"] = options_dict
        return result

    # Check Player State
    def is_player_end(self):
        game_result = False
        # TODO only check player 1 now
        hands = self.now_player.get_hands()
        if hands:
            game_result = all([(True if hand.result != "" else False) for hand in hands])
        return game_result

    # Show Game End
    def show_hand_result(self):

        game_result = ""
        # TODO only check player 1 now
        hands = self.now_player.get_hands()
        for num in range(len(hands)):
            if num != 0:
                game_result += ", "
            if hands[num].get_result() == "push":
                game_result += "PUSH"
            elif hands[num].get_result() == "blackjack":
                game_result += "BlackJack"
            elif hands[num].get_result() == "lose":
                game_result += "LOSE"
            elif hands[num].get_result() == "win":
                game_result += "WIN"
        return game_result

    def show_game_end(self):

        q_config = {"font": ("Arial", 30, "bold")}
        r_config = {"font": ("Arial", 18, "bold")}
        o_config = [{"font": ("Arial", 18, "bold")}, {"font": ("Arial", 18, "bold")}]

        if self.game_state == "no money":
            x = 243
            y = 130
            game_result = "Not Enough Money"
            options = ["Quit"]
        else:
            x = 300
            y = 150
            game_result = self.show_hand_result()
            options = ["Continue", "Quit"]

        # Create Area
        result = self.show_question(x, y, question=f"Game End", q_config=q_config,
                                    game_result=f"Result: {game_result}", r_config=r_config,
                                    options=options, o_index=["continue", "quit"], o_config=o_config)

        self.game_interface_dict[self.game_state] = result

    # Show Card
    def show_card(self, x, y, card_loc, faced):

        if faced:
            return self.table_canvas.create_image(x, y, image=self.table_canvas.cards[card_loc], anchor="nw")
        else:
            return self.table_canvas.create_image(x, y, image=self.table_canvas.cards[0], anchor="nw")

    def show_banker_card(self):

        # Delete the previous card img
        if self.banker_img:
            self.delete_imgs(self.banker_img)
            self.banker_img = []

        # Create card img
        cards = self.game.banker
        for card_num in range(len(cards)):
            card = cards[card_num]
            card_spce = 48 if card_num != 0 else 0
            card_loc = 14 * self.img_suit_dict[card.suit] + self.img_symbol_dict[card.symbol]
            self.banker_img.append(
                self.show_card(325 + card_spce + 20 * card_num + CARD_HORIZONTAL_MODIFY, 30, card_loc, card.faced))

    def show_players_card(self):

        # Create card img
        for player_num in range(self.player_num):
            self.show_player_card(player_num,
                                  self.players_area_xy[player_num][0],
                                  self.players_area_xy[player_num][1])

    def show_player_card(self, player_num, x, y):

        # Delete the previous card img
        if self.players_img:
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
                card_img = self.show_card(x + 20 * card_num + CARD_HORIZONTAL_MODIFY,
                                          y + IMG_HAND_CARD_SPACE * hand_num, card_loc,
                                          card.faced)
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
        choices[pre_choice][0].config(fg="white", bg="black")
        choices[now_choice][0].config(fg="black", bg="white")
        return now_choice

    # banker time
    def banker_time(self):
        self.game.reveal_banker_card()
        self.game.deal_to_banker()
        self.show_banker_card()
        if self.game.get_is_banker_bust():
            self.game.banker_bust_process()
        else:
            self.game.compare_cards()
        self.game_end_process()

    # Keyboard
    def upKey(self, event):
        if self.game_state == "insurance":
            self.is_insurance = True
            self.game_choice = self.switch_choice(self.game_choice, "up",
                                                  self.game_interface_dict[self.game_state]["options"])
        elif self.game_state == "choice":
            self.game_choice = self.switch_choice(self.game_choice, "up",
                                                  self.game_interface_dict[self.game_state]["options"])
        elif self.game_state == "end":
            self.game_choice = self.switch_choice(self.game_choice, "up",
                                                  self.game_interface_dict[self.game_state]["options"])
        print("Up key pressed")

    def downKey(self, event):
        if self.game_state == "insurance":
            self.is_insurance = False
            self.game_choice = self.switch_choice(self.game_choice, "down",
                                                  self.game_interface_dict[self.game_state]["options"])
        elif self.game_state == "choice":
            self.game_choice = self.switch_choice(self.game_choice, "down",
                                                  self.game_interface_dict[self.game_state]["options"])
        elif self.game_state == "end":
            self.game_choice = self.switch_choice(self.game_choice, "down",
                                                  self.game_interface_dict[self.game_state]["options"])
        print("Down key pressed")

    def leftKey(self, event):
        print("Left key pressed")

    def rightKey(self, event):
        print("Right key pressed")

    def enterKey(self, event):

        if self.game_state == "insurance":
            self.game.ask_insurance(self.is_insurance)
            # Destroy previous Area
            self.destroy_obj(self.game_interface_dict["insurance"]["area"])
            self.game_state = "blackjack"
            self.check_blackjack()

        elif self.game_state == "choice":

            game_choice_ = self.game_interface_dict[self.game_state]["options"][self.game_choice][1]
            if game_choice_ == "double":
                # ToDo Only Player 1
                self.game.double_down_process(self.now_player)
                self.show_players_card()
                self.destroy_obj(self.game_interface_dict["choice"]["area"])
                if self.is_player_end():
                    self.game_state = "end"
                    self.game_choice = 0
                    self.show_game_end()
                else:
                    self.game_state = "banker"
                    self.banker_time()

            elif game_choice_ == "split":
                # ToDo Only Player 1 Hand 1
                self.game.split_process(self.now_player, self.now_player.get_hands()[0])
                self.show_players_card()
                self.destroy_obj(self.game_interface_dict["choice"]["area"])
                self.player_choice(self.now_player)

            elif game_choice_ == "hit":
                self.set_player_hit(self.now_player)
                self.show_players_card()
                self.destroy_obj(self.game_interface_dict["choice"]["area"])
                if self.is_player_end():
                    self.game_state = "end"
                    self.game_choice = 0
                    self.show_game_end()
                else:
                    self.player_choice(self.now_player)

            elif game_choice_ == "stand":
                self.destroy_obj(self.game_interface_dict["choice"]["area"])
                self.set_player_stand(self.now_player)
                if self.is_player_end():
                    self.game_state = "banker"
                    self.banker_time()
                else:
                    self.player_choice(self.now_player)

        elif self.game_state == "end":

            game_choice_ = self.game_interface_dict[self.game_state]["options"][self.game_choice][1]
            if game_choice_ == "continue":
                # Destroy previous Area
                self.destroy_obj(self.game_interface_dict["end"]["area"])
                self.game_start()
            elif game_choice_ == "quit":
                self.table_canvas.delete("all")
                welcome_ = welcome.Welcome(self.game, self.window, self.table_canvas, self.window_width,
                                           self.window_height, self.padding)
                del self
        elif self.game_state == "no money":
            self.table_canvas.delete("all")
            welcome_ = welcome.Welcome(self.game, self.window, self.table_canvas, self.window_width,
                                       self.window_height, self.padding)
            del self
        print("Enter key pressed")
