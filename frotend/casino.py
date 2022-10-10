import pyglet
from tkinter import *
from PIL import Image, ImageTk

IMG_LEFT_BOUND = 10
IMG_UP_BOUND = 10
IMG_HORIZONTAL_SPACE = 63
IMG_VERTICAL_SPACE = 94
IMG_HORIZONTAL_INTERVAL = 2
IMG_VERTICAL_INTERVAL = 2


class Casino:

    def __init__(self, game, window, canvas, window_width, window_height, padding):

        # Game instance
        self.game = game

        # Game Attribute
        self.deck_num = self.game.get_deck_num()
        self.player_num = self.game.get_player_num()
        self.min_bet = self.game.get_min_bet()
        self.is_insurance = self.game.get_is_insurance()
        self.is_over_ten = self.game.get_insurance_over_10()
        self.is_double = self.game.get_is_double()
        self.blackjack_ratio = self.game.get_blackjack_ratio()

        self.players = self.game.get_player()

        # Attribute
        self.window = window
        self.window_width = window_width
        self.window_height = window_height
        self.padding = padding
        self.table_canvas = canvas

        # Table Image
        table_img = Image.open("../img/pixel-blackjack_big.png")
        table_img = table_img.resize((800, 400))
        self.table_canvas.table_pic = ImageTk.PhotoImage(table_img)
        self.table_canvas.create_image(400, 200, image=self.table_canvas.table_pic)

        # Card Image
        card_img_map = Image.open("../img/poker_card.png")

        card_img_map = card_img_map.resize((1000, 400))
        card_img_map_x = [(10, 73), (74, 137), (138, 201), (203, 266), (267, 330), (332, 394), (396, 359), (460, 523),
                      (524, 587), (589, 652), (653, 716), (718, 780), (782, 845), (846, 909)]
        card_img_map_y = [(11, 104), (106, 200), (202, 294), (296, 389)]
        self.card_coordinates = [(x[0], y[0], x[1], y[1]) for x in card_img_map_x for y in card_img_map_y]

        # self.card_img_list = []
        # for num in range(len(self.card_coordinates)):
        #     card_coordinate = self.card_coordinates[num]
        #     slice_img = card_img_map.crop(card_coordinate)
        #     self.table_canvas.card = ImageTk.PhotoImage(slice_img)
        #     self.card_img_list.append(ImageTk.PhotoImage(slice_img))


        img1 = ImageTk.PhotoImage(card_img_map.crop(self.card_coordinates[0]))
        # img2 = ImageTk.PhotoImage(card_img_map.crop(self.card_coordinates[2]))
        # img3 = ImageTk.PhotoImage(card_img_map.crop(self.card_coordinates[3]))
        # self.card_img_list.append(img1)
        # self.card_img_list.append(img2)
        # self.card_img_list.append(img3)
        self.table_canvas.create_image(400, 100, image=img1)
        # self.table_canvas.create_image(400, 200, image=self.card_img_list[1])
        # self.table_canvas.create_image(400, 300, image=self.card_img_list[2])
        # Banker Area
        banker_area = self.table_canvas.create_rectangle(325, 30, 475, 130, outline="black", width=3)

        # Player Area
        player_area = []
        if self.player_num == 1:
            player_area.append(self.table_canvas.create_rectangle(350, 260, 450, 340, outline="black", width=3))
        elif self.player_num == 2:
            player_area.append(self.table_canvas.create_rectangle(150, 230, 250, 310, outline="black", width=3))
            player_area.append(self.table_canvas.create_rectangle(550, 230, 650, 310, outline="black", width=3))
        elif self.player_num == 3:
            player_area.append(self.table_canvas.create_rectangle(120, 230, 220, 310, outline="black", width=3))
            player_area.append(self.table_canvas.create_rectangle(350, 260, 450, 340, outline="black", width=3))
            player_area.append(self.table_canvas.create_rectangle(580, 230, 680, 310, outline="black", width=3))

        # Game start
        self.game.start()
        self.show_player_card()

    def show_player_card(self):

        img_suit_dict = {"heart": 0, "club": 1, "diamond": 2, "spade": 3}
        img_symbol_dict = {"faced": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7, "9": 8, "10": 9, "J": 10,
                           "Q": 11, "K": 12, "A": 13}

        # for num in range(len(self.players)):
        #     hand = self.players[num].get_hands()
        # hands = self.players[0].get_hands()
        # for hand_num in range(len(hands)):
        #     hand = hands[hand_num]
        #     cards = hand.cards
        #     for card_num in range(len(cards)):
        #         print(card_num)
        #         card = cards[card_num]
        #         card_loc = 14 * img_suit_dict[card.suit] + img_symbol_dict[card.symbol]
        #         # print(self.card_img_list[0], self.table_canvas.card )
        #         # self.table_canvas.create_image(400, 200, image=self.card_img_list[card_loc])
        #         self.table_canvas.create_image(400 + 70 * card_num, 200, image=self.table_canvas.card)
        # print(1)