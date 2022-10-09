import pyglet
from tkinter import *
from PIL import Image, ImageTk


PIXEL_FONT = pyglet.font.add_file('../font/Pixels.ttf')

TITLE_FONT = ("Pixels", 120, "bold")
CHOICE_FONT = ("Arial", 24, "bold")
COPY_RIGHT_FONT = ("Arial", 12, "italic")

class Welcome:

    def __init__(self, window, canvas, window_width, window_height, padding):

        self.welcome_state = 0
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

        # Title
        self.game_title = self.table_canvas.create_text(400, 100, text="Blackjack ", font=TITLE_FONT,
                                                        fill="white")
        self.title_icon = self.table_canvas.create_text(590, 115, text="♠", font=("Pixels", 80, "bold"))

        # Choice
        self.choice_icon = self.table_canvas.create_text(330, 200, text="♦", font=CHOICE_FONT, fill="red")
        self.start = self.table_canvas.create_text(350, 200, text="Start", font=CHOICE_FONT, fill="white",
                                                   anchor=W)
        self.setting = self.table_canvas.create_text(350, 250, text="Setting", font=CHOICE_FONT, anchor=W)
        self.quit_ = self.table_canvas.create_text(350, 300, text="Quit", font=CHOICE_FONT, anchor=W)

        # Copy Right
        self.copy_right = self.table_canvas.create_text(770-self.padding, 400-self.padding, text="©Jim 2022 ", font=COPY_RIGHT_FONT)

        self.table_canvas.grid(column=1, row=1)
        self.welcome_interface()

    def toggle_color(self, canvas, item, color_a, color_b):
        if canvas.itemcget(item, "fill") == color_a:
            canvas.itemconfig(item, fill=color_b)
        else:
            canvas.itemconfig(item, fill=color_a)

    def change_icon_loc(self, canvas, item, state_, x, y):
        canvas.moveto(item, x, y + 50 * (state_ - 1))

    def blink(self, canvas, item, delay_time):
        self.toggle_color(canvas, item, "black", "white")
        self.window.after(delay_time, self.blink, canvas, item, delay_time)

    def switch_choice(self, pre_state, state_):
        canvas = self.table_canvas
        self.toggle_color(canvas, self.state_to_item(pre_state), "black", "white")
        self.toggle_color(canvas, self.state_to_item(state_), "black", "white")
        self.change_icon_loc(canvas, self.choice_icon, state_, 300 + self.padding, 250 - self.padding)

    def state_to_item(self, state_):
        if state_ == 0:
            return self.start
        elif state_ == 1:
            return self.setting
        else:
            return self.quit_

    def upKey(self, event):

        pre_state = self.welcome_state
        if self.welcome_state > 0:
            self.welcome_state -= 1
        self.switch_choice(pre_state, self.welcome_state)
        print("Up key pressed")

    def downKey(self, event):

        pre_state = self.welcome_state
        if self.welcome_state < 2:
            self.welcome_state += 1
        self.switch_choice(pre_state, self.welcome_state)
        print("Down key pressed")

    def leftKey(self, event):
        print("Left key pressed")

    def rightKey(self, event):
        print("Right key pressed")

    def enterKey(self, event):

        if self.welcome_state == 0:
            pass
        elif self.welcome_state == 1:
            self.table_canvas.delete("all")
        else:
            self.window.destroy()
        print("Enter key pressed")

    # Show Table
    def welcome_interface(self):

        self.blink(self.table_canvas, self.game_title, 1000)

        self.window.bind('<Up>', self.upKey)
        self.window.bind('<Down>', self.downKey)
        self.window.bind('<Return>', self.enterKey)
