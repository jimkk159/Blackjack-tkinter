from tkinter import *

# self module
from public import *

WHITE = "#DBDBDB"
CHOICE_FONT = ("Arial", 24, "bold")


class Setting:

    def __init__(self, window, canvas, window_width, window_height, padding):

        self.state_dict = {"deck": [0, 0], "player": [0, 1], "bet": [0, 2], "insurance": [0, 3], "over_ten": [0, 4],
                           "double_down": [0, 5], "bj": [1, 0], "choose": [2, 0], "cancel": [2, 1], "quit": [2, 2]}
        self.setting_state = [0, 0]
        self.window = window
        self.window_width = window_width
        self.window_height = window_height
        self.padding = padding
        self.setting_canvas = canvas
        self.setting_canvas.config(highlightthickness=5)

        self.deck_num = 4

        # Setting Argument
        self.setting_argument = Frame(self.window, background="red", highlightthickness=5)
        self.deck_num = self.setting_canvas.create_text(30, 50, text="Deck Number: 8", font=CHOICE_FONT, anchor=W,
                                                        fill="#DBDBDB")
        self.player_num = self.setting_canvas.create_text(30, 110, text="Player Number: 2", font=CHOICE_FONT, anchor=W,
                                                          fill=WHITE)
        self.min_bet = self.setting_canvas.create_text(30, 170, text="Minium Bet: 5", font=CHOICE_FONT, anchor=W,
                                                       fill=WHITE)
        self.is_insurance = self.setting_canvas.create_text(30, 230, text="Insurance: Open", font=CHOICE_FONT, anchor=W,
                                                            fill=WHITE)
        self.over_ten = self.setting_canvas.create_text(30, 290, text="Over 10 Insurance: Open", font=CHOICE_FONT,
                                                        anchor=W, fill=WHITE)
        self.is_double_down = self.setting_canvas.create_text(30, 350, text="Double Down: Open", font=CHOICE_FONT,
                                                              anchor=W, fill=WHITE)
        self.bj_ratio = self.setting_canvas.create_text(450, 50, text="BlackJack ration:1.5", font=CHOICE_FONT,
                                                        anchor=W, fill=WHITE)

        # Setting Control
        self.setting_control = Frame(self.window, background="black", highlightthickness=5)
        self.setting_window = self.setting_canvas.create_window(640, 230, width=148, height=160,
                                                                window=self.setting_control, anchor='nw')
        self.choose = Label(self.setting_control, text="Choose", width=6, bd=0, font=CHOICE_FONT, anchor=W, bg="black",
                            fg=WHITE)
        self.choose.grid(column=0, row=0, padx=(self.padding / 2, self.padding / 2),
                         pady=(self.padding / 2, self.padding / 4))
        self.cancel = Label(self.setting_control, text="Cancel", width=6, bd=0, font=CHOICE_FONT, anchor=W, bg="black",
                            fg=WHITE)
        self.cancel.grid(column=0, row=1, padx=(self.padding / 2, self.padding / 2),
                         pady=self.padding / 4)
        self.quit_ = Label(self.setting_control, text="Quit", width=6, bd=0, font=CHOICE_FONT, anchor=W, bg="black",
                           fg=WHITE)
        self.quit_.grid(column=0, row=2, padx=(self.padding / 2, self.padding / 2),
                        pady=(self.padding / 4, self.padding / 2))
        # Choice
        self.choice_icon = self.setting_canvas.create_text(329, 198, text="♥", font=CHOICE_FONT, fill="red")

        # self.control_setting()

    # def switch_choice(self, state_):
    #     canvas = self.setting_canvas
    #     for i in range(len(self.state_dict)):
    #         if i == state_:
    #             canvas.itemconfig(self.state_to_item(i), fill=WHITE)
    #         else:
    #             canvas.itemconfig(self.state_to_item(i), fill="black")
    #     # self.change_icon_loc(canvas, self.choice_icon, state_, 300 + self.padding, 250 - self.padding)

    # Keyboard
    def upKey(self, event):
        x, y = self.setting_state
        if y > 0:
            y -= 1
        self.setting_state = [x, y]
        # self.switch_state(self.setting_state)
        print("Up key pressed", x, y)

    def downKey(self, event):
        x, y = self.setting_state
        if x == 0 and y < 5:
            y += 1
        elif x == 2 and y < 2:
            y += 1
        self.setting_state = [x, y]
        print("Down key pressed", x, y)

    def leftKey(self, event):
        x, y = self.setting_state
        if x > 0:
            x -= 1
        self.setting_state = [x, y]
        if x == 1:
            y = 0
        print("Left key pressed", x, y)

    def rightKey(self, event):
        x, y = self.setting_state
        if x < 2:
            x += 1
        if x == 1:
            y = 0
        if x == 2 and y > 2:
            y = 2
        self.setting_state = [x, y]
        print("Right key pressed", x, y)

    # def enterKey(self, event):
    #
    #     if self.welcome_state == 0:
    #         print("start")
    #         self.start_choice()
    #     elif self.welcome_state == 1:
    #         print("setting")
    #         self.table_canvas.delete("all")
    #         self.setting_choice()
    #     else:
    #         print("quit")
    #         self.quit_choice()
    #     print("Enter key pressed")

    # Control Table
    def control_setting(self):
        start_blink(self.window, self.setting_canvas, self.choose, 1000, True)
        self.window.bind('<Up>', self.upKey)
        self.window.bind('<Down>', self.downKey)
        self.window.bind('<Left>', self.leftKey)
        self.window.bind('<Right>', self.rightKey)
        # self.window.bind('<Return>', self.enterKey)
