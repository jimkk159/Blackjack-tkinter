from tkinter import *

# self module
from public import *
import welcome

WHITE = "#DBDBDB"
CHOICE_FONT = ("Arial", 24, "bold")
QUIT_FONT = ("Arial", 30, "italic")
ARROW_FONT = ("Arial", 40, "bold")

LEFT_ANCHOR = 50
HORIZONTAL_SPACE = 400

UP_ANCHOR = 50
VERTICAL_SPACE = 60


class Setting:

    def __init__(self, window, canvas, window_width, window_height, padding):

        self.setting_state_dict = {"choice": 0, "modify": 1}
        self.setting_state = 0
        self.choice_state_dict = {"deck": [0, 0], "player": [0, 1], "bet": [0, 2], "insurance": [0, 3],
                                  "over_ten": [0, 4],
                                  "double_down": [0, 5], "blackjack": [1, 0], "quit": [1, 1]}
        self.choice_state = [0, 0]
        self.window = window
        self.window_width = window_width
        self.window_height = window_height
        self.padding = padding
        self.setting_canvas = canvas
        self.setting_canvas.config(highlightthickness=5)

        # Setting Argument
        self.setting_argument = Frame(self.window, background="red", highlightthickness=5)
        self.deck = self.setting_canvas.create_text(LEFT_ANCHOR, UP_ANCHOR, text="Deck Number:", font=CHOICE_FONT,
                                                    anchor=W, fill=WHITE)
        self.deck_num = self.setting_canvas.create_text(LEFT_ANCHOR + 225, UP_ANCHOR, text="4", font=CHOICE_FONT,
                                                        anchor=W, fill=WHITE)
        self.player = self.setting_canvas.create_text(LEFT_ANCHOR, UP_ANCHOR + VERTICAL_SPACE,
                                                      text="Player Number:", font=CHOICE_FONT, anchor=W, fill=WHITE)
        self.player_num = self.setting_canvas.create_text(LEFT_ANCHOR + 245, UP_ANCHOR + VERTICAL_SPACE,
                                                          text="2", font=CHOICE_FONT, anchor=W, fill=WHITE)
        self.bet = self.setting_canvas.create_text(LEFT_ANCHOR, UP_ANCHOR + 2 * VERTICAL_SPACE,
                                                   text="Minium Bet:", font=CHOICE_FONT, anchor=W,
                                                   fill=WHITE)
        self.bet_num = self.setting_canvas.create_text(LEFT_ANCHOR + 190, UP_ANCHOR + 2 * VERTICAL_SPACE,
                                                       text="8", font=CHOICE_FONT, anchor=W,
                                                       fill=WHITE)
        self.insurance = self.setting_canvas.create_text(LEFT_ANCHOR, UP_ANCHOR + 3 * VERTICAL_SPACE,
                                                         text="Insurance:", font=CHOICE_FONT, anchor=W, fill=WHITE)
        self.is_insurance = self.setting_canvas.create_text(LEFT_ANCHOR + 165, UP_ANCHOR + 3 * VERTICAL_SPACE,
                                                            text="Close", font=CHOICE_FONT, anchor=W,
                                                            fill=WHITE)
        self.over_ten = self.setting_canvas.create_text(LEFT_ANCHOR, UP_ANCHOR + 4 * VERTICAL_SPACE,
                                                        text="Over 10 Insurance:", font=CHOICE_FONT,
                                                        anchor=W, fill=WHITE)
        self.is_over_ten = self.setting_canvas.create_text(LEFT_ANCHOR + 290, UP_ANCHOR + 4 * VERTICAL_SPACE,
                                                           text="Close", font=CHOICE_FONT,
                                                           anchor=W, fill=WHITE)
        self.double_down = self.setting_canvas.create_text(LEFT_ANCHOR, UP_ANCHOR + 5 * VERTICAL_SPACE,
                                                           text="Double Down:", font=CHOICE_FONT,
                                                           anchor=W, fill=WHITE)
        self.is_double_down = self.setting_canvas.create_text(LEFT_ANCHOR + 220, UP_ANCHOR + 5 * VERTICAL_SPACE,
                                                              text="Close", font=CHOICE_FONT,
                                                              anchor=W, fill=WHITE)
        self.blackjack = self.setting_canvas.create_text(LEFT_ANCHOR + HORIZONTAL_SPACE, UP_ANCHOR,
                                                         text="BlackJack ration:", font=CHOICE_FONT,
                                                         anchor=W, fill=WHITE)
        self.blackjack_ratio = self.setting_canvas.create_text(LEFT_ANCHOR + HORIZONTAL_SPACE + 275, UP_ANCHOR,
                                                               text="1.2", font=CHOICE_FONT,
                                                               anchor=W, fill=WHITE)
        self.leave = self.setting_canvas.create_text(650, 360, text="Leave", font=QUIT_FONT,
                                                     anchor=W, fill=WHITE)

        # Instruction️
        self.instruction_return = self.setting_canvas.create_text(740, 280,
                                                                 text="↩",
                                                                 font=("Arial", 50, "bold"),
                                                                 fill=WHITE)
        self.instruction = self.setting_canvas.create_text(740, 240,
                                                                 text="Confirm: ",
                                                                 font=("Arial", 16, "italic"),
                                                                 fill=WHITE)

        self.arrow_up = self.setting_canvas.create_text(600, 180,
                                                        text="↑",
                                                        font=ARROW_FONT,
                                                        fill=WHITE)
        self.arrow_down = self.setting_canvas.create_text(600, 260,
                                                          text="↓",
                                                          font=ARROW_FONT,
                                                          fill=WHITE)
        self.arrow_left = self.setting_canvas.create_text(560, 220,
                                                          text="←",
                                                          font=ARROW_FONT,
                                                          fill=WHITE)
        self.arrow_right = self.setting_canvas.create_text(640, 220,
                                                           text="→",
                                                           font=ARROW_FONT,
                                                           fill=WHITE)
        # Choice
        self.choice_icon = self.setting_canvas.create_text(LEFT_ANCHOR - self.padding, UP_ANCHOR, text="♥",
                                                           font=CHOICE_FONT,
                                                           fill="red")

        self.control_setting()

    def change_icon_loc(self, canvas, item, state_, x, y):
        state_x, state_y = state_
        if state_x == 1 and state_y == 1:
            x += 200
            y += 10
            state_y = 5
        canvas.moveto(item, x + state_x * HORIZONTAL_SPACE - 10, y + state_y * VERTICAL_SPACE + 2)

    def switch_choice(self, state_):
        x, y = state_
        canvas = self.setting_canvas
        self.change_icon_loc(canvas, self.choice_icon, state_, LEFT_ANCHOR - self.padding, UP_ANCHOR - self.padding)

    # Choice
    def start_choice(self):
        pass

    def leave_choice(self):
        self.setting_canvas.delete("all")
        stop_blink(self.window)
        welcome_ = welcome.Welcome(self.window, self.setting_canvas, self.window_width, self.window_height,
                                   self.padding)

    def quit_choice(self):
        self.window.destroy()

    # Keyboard
    def upKey(self, event):
        if self.setting_state == self.setting_state_dict["choice"]:
            x, y = self.choice_state
            if y > 0:
                y -= 1
            self.choice_state = [x, y]
            self.switch_choice(self.choice_state)
        print("Up key pressed")

    def downKey(self, event):
        if self.setting_state == self.setting_state_dict["choice"]:
            x, y = self.choice_state
            if x == 0 and y < 5:
                y += 1
            elif x == 1 and y < 1:
                y += 1
            self.choice_state = [x, y]
            self.switch_choice(self.choice_state)
        print("Down key pressed")

    def leftKey(self, event):
        if self.setting_state == self.setting_state_dict["choice"]:
            x, y = self.choice_state

            if x == 1 and y == 1:
                y = 5

            if x > 0:
                x -= 1

            self.choice_state = [x, y]
            self.switch_choice(self.choice_state)
        print("Left key pressed")

    def rightKey(self, event):
        if self.setting_state == self.setting_state_dict["choice"]:
            x, y = self.choice_state

            if x == 0 and y < 2:
                y = 0
            elif x == 0 and y >= 2:
                y = 1

            if x < 1:
                x += 1

            self.choice_state = [x, y]
            self.switch_choice(self.choice_state)
        print("Right key pressed")

    def enterKey(self, event):

        if self.setting_state == self.setting_state_dict["choice"]:
            self.setting_state = self.setting_state_dict["modify"]
            if self.choice_state == [0, 0]:
                start_blink(self.window, self.setting_canvas, self.deck_num, 1000, 750)
                print("deck")
            elif self.choice_state == [0, 1]:
                start_blink(self.window, self.setting_canvas, self.player_num, 1000, 750)
                print("player")
            elif self.choice_state == [0, 2]:
                start_blink(self.window, self.setting_canvas, self.bet_num, 1000, 750)
                print("bet")
            elif self.choice_state == [0, 3]:
                start_blink(self.window, self.setting_canvas, self.is_insurance, 1000, 750)
                print("insurance")
            elif self.choice_state == [0, 4]:
                start_blink(self.window, self.setting_canvas, self.is_over_ten, 1000, 750)
                print("over_ten")
            elif self.choice_state == [0, 5]:
                start_blink(self.window, self.setting_canvas, self.is_double_down, 1000, 750)
                print("double_down")
            elif self.choice_state == [1, 0]:
                start_blink(self.window, self.setting_canvas, self.blackjack_ratio, 1000, 750)
                print("blackjack")
            else:
                self.leave_choice()
                print("leave")
        else:
            self.setting_state = self.setting_state_dict["choice"]
            stop_blink(self.window)
            item = None
            if self.choice_state == [0, 0]:
                item = self.deck_num
            elif self.choice_state == [0, 1]:
                item = self.player_num
            elif self.choice_state == [0, 2]:
                item = self.bet_num
            elif self.choice_state == [0, 3]:
                item = self.is_insurance
            elif self.choice_state == [0, 4]:
                item = self.is_over_ten
            elif self.choice_state == [0, 5]:
                item = self.is_double_down
            elif self.choice_state == [1, 0]:
                item = self.blackjack_ratio
            self.setting_canvas.itemconfig(item, fill=WHITE)
        print("Enter key pressed")

    # Control Table
    def control_setting(self):
        self.window.bind('<Up>', self.upKey)
        self.window.bind('<Down>', self.downKey)
        self.window.bind('<Left>', self.leftKey)
        self.window.bind('<Right>', self.rightKey)
        self.window.bind('<Return>', self.enterKey)
