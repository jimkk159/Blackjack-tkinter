from tkinter import *

# self module
from welcome import Welcome
from game import Blackjack
from setting import Setting

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

PADDING = 20


class Frontend:

    def __init__(self):
        self.window = Tk()
        self.window.maxsize(840, 440)
        self.window.resizable(False, False)
        self.window.state('zoomed')
        self.window.title("Jim's Blackjack Game")
        self.window.minsize(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.window.config(padx=PADDING, pady=PADDING, bg="black")

        # Game Icon
        self.window.iconbitmap("../icon/poker-cards.ico")

        game = Blackjack()

        self.canvas = Canvas(self.window, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
                             highlightthickness=0)
        welcome = Welcome(game, self.window, self.canvas, WINDOW_WIDTH, WINDOW_HEIGHT, PADDING)
        # setting = Setting(self.window, self.canvas, WINDOW_WIDTH, WINDOW_HEIGHT, PADDING)
        self.window.mainloop()


frontend = Frontend()
