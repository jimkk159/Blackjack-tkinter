from tkinter import *
from PIL import Image, ImageTk

from card import Card

CHOICE_FONT = ("Arial", 10, "bold")

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
        self.is_insurance = self.game.get_is_insurance()
        self.is_over_ten = self.game.get_insurance_over_10()
        self.is_double = self.game.get_is_double()
        self.blackjack_ratio = self.game.get_blackjack_ratio()
        self.players = self.game.get_player()

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
        self.game_state = ""


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

        self.control_casino()
        self.game_start()

    def game_start(self):

        # while not self.game.game_end:
        # Game start
        self.game.reset()
        self.game.deal_to_all()
        self.game.banker = [Card(symbol='K', suit='spade'),
                            Card(symbol='A', suit='heart')]
        self.show_banker_card()
        self.show_player_card()

        if self.is_insurance:
            self.ask_insurance()

    def ask_insurance(self):

        self.game_state = "insurance"
        if self.game.banker[1].symbol == "A" or (
                self.is_over_ten and self.game.banker[1].symbol in ["A", "K", "Q", "J", "10"]):
            # for num in range(self.player_num):
            x1, y1, x2, y2 = self.players_area_xy[0]
            frame = Frame(self.window, height=100, width=100, bg="black")
            frame.grid()
            insurance_question = Label(frame, text="Buy insurance?", fg="white", bg="black", font=CHOICE_FONT)
            insurance_question.grid(column=0, row=0)
            insurance_choice_yes = Label(frame, text="Yes", fg="black", bg="white", font=CHOICE_FONT)
            insurance_choice_yes.grid(column=0, row=1)
            insurance_choice_no = Label(frame, text="No", fg="white", bg="black", font=CHOICE_FONT)
            insurance_choice_no.grid(column=0, row=2)
            insurance_area = self.table_canvas.create_window(x1 - 130, y1, window=frame, anchor="nw")
            # insurance_area = self.table_canvas.create_rectangle(x1 - 130, y1, x2 - 130, y2, outline="black",
            #                                                     width=3)

    def show_card(self, x, y, card_loc, faced):

        if faced:
            self.table_canvas.create_image(x, y, image=self.table_canvas.cards[card_loc], anchor="nw")
        else:
            self.table_canvas.create_image(x, y, image=self.table_canvas.cards[0], anchor="nw")

    def show_banker_card(self):

        cards = self.game.banker
        for card_num in range(len(cards)):
            card = cards[card_num]
            print(card.suit, card.symbol, self.img_suit_dict[card.suit], self.img_symbol_dict[card.symbol])
            card_loc = 14 * self.img_suit_dict[card.suit] + self.img_symbol_dict[card.symbol]
            self.show_card(325 + 68 * card_num + CARD_HORIZONTAL_MODIFY, 30, card_loc, card.faced)

    def show_player_card(self):

        for player_num in range(self.player_num):
            hands = self.players[player_num].get_hands()
            for hand_num in range(len(hands)):
                hand = hands[hand_num]
                cards = hand.cards
                for card_num in range(len(cards)):
                    card = cards[card_num]
                    card_loc = 14 * self.img_suit_dict[card.suit] + self.img_symbol_dict[card.symbol]
                    self.show_card(self.players_area_xy[player_num][0] + 68 * card_num + CARD_HORIZONTAL_MODIFY,
                                   self.players_area_xy[player_num][1],
                                   card_loc,
                                   card.faced)

    # Control Table
    def control_casino(self):
        self.window.bind('<Up>', self.upKey)
        self.window.bind('<Down>', self.downKey)
        self.window.bind('<Left>', self.leftKey)
        self.window.bind('<Right>', self.rightKey)
        self.window.bind('<Return>', self.enterKey)