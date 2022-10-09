import pyglet
from tkinter import *
from setting import Setting
from PIL import Image, ImageTk

PIXEL_FONT = pyglet.font.add_file('../font/Pixels.ttf')

TITLE_FONT = ("Pixels", 120, "bold")
CHOICE_FONT = ("Arial", 24, "bold")
COPY_RIGHT_FONT = ("Arial", 12, "italic")


class Welcome:

    def __init__(self, window, canvas, window_width, window_height, padding):

        self.state_dict = {"start": 0, "setting": 1, "quit": 2}
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
        # Why has the 1px border
        self.choice_icon = self.table_canvas.create_text(329, 198, text="♦", font=CHOICE_FONT, fill="red")
        self.start = self.table_canvas.create_text(350, 200, text="Start", font=CHOICE_FONT, fill="white",
                                                   anchor=W)
        self.setting = self.table_canvas.create_text(350, 250, text="Setting", font=CHOICE_FONT, anchor=W)
        self.quit_ = self.table_canvas.create_text(350, 300, text="Quit", font=CHOICE_FONT, anchor=W)

        # Copy Right
        self.copy_right = self.table_canvas.create_text(770 - self.padding, 400 - self.padding, text="©Jim 2022 ",
                                                        font=COPY_RIGHT_FONT)

        self.table_canvas.grid(column=1, row=1)
        self.control_welcome()

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

    def switch_choice(self, state_):
        canvas = self.table_canvas
        for i in range(len(self.state_dict)):
            if i == state_:
                canvas.itemconfig(self.state_to_item(i), fill="white")
            else:
                canvas.itemconfig(self.state_to_item(i), fill="black")
        self.change_icon_loc(canvas, self.choice_icon, state_, 300 + self.padding, 250 - self.padding)

    def state_to_item(self, state_):
        if state_ == 0:
            return self.start
        elif state_ == 1:
            return self.setting
        else:
            return self.quit_

    # Choice
    def start_choice(self):
        pass

    def setting_choice(self):
        self.table_canvas.delete("all")
        setting = Setting(self.window, self.table_canvas, self.window_width, self.window_height, self.padding)

    def quit_choice(self):
        self.window.destroy()

    # Keyboard
    def upKey(self, event):
        if self.welcome_state > 0:
            self.welcome_state -= 1
        self.switch_choice(self.welcome_state)
        print("Up key pressed")

    def downKey(self, event):

        if self.welcome_state < 2:
            self.welcome_state += 1
        self.switch_choice(self.welcome_state)
        print("Down key pressed")

    def leftKey(self, event):
        print("Left key pressed")

    def rightKey(self, event):
        print("Right key pressed")

    def enterKey(self, event):

        if self.welcome_state == 0:
            print("start")
            self.start_choice()
        elif self.welcome_state == 1:
            print("setting")
            self.table_canvas.delete("all")
            self.setting_choice()
        else:
            print("quit")
            self.quit_choice()
        print("Enter key pressed")

    # Mouse
    def mouseClick(self, event):

        if 450 > event.x > 300 and 225 >= event.y > 175:
            print("start")
            self.start_choice()
        elif 500 > event.x > 300 and 275 >= event.y > 225:
            print("setting")
            self.setting_choice()
        elif 450 > event.x > 300 and 325 >= event.y > 275:
            print("quit")
            self.quit_choice()

        print("Mouse Click position:", event.x, event.y)

    def mouseMotion(self, event):

        print("Motion", event.x, event.y)
        if 450 > event.x > 300 and 225 >= event.y > 175:
            self.switch_choice(self.state_dict["start"])
            self.change_icon_loc(self.table_canvas,
                                 self.choice_icon,
                                 self.state_dict["start"],
                                 300 + self.padding,
                                 250 - self.padding)
        elif 500 > event.x > 300 and 275 >= event.y > 225:
            self.switch_choice(self.state_dict["setting"])
            self.change_icon_loc(self.table_canvas,
                                 self.choice_icon,
                                 self.state_dict["setting"],
                                 300 + self.padding,
                                 250 - self.padding)
        elif 450 > event.x > 300 and 325 >= event.y > 275:
            self.switch_choice(self.state_dict["quit"])
            self.change_icon_loc(self.table_canvas,
                                 self.choice_icon,
                                 self.state_dict["quit"],
                                 300 + self.padding,
                                 250 - self.padding)
        print("Mouse Move position", event.x, event.y)

    # Control Table
    def control_welcome(self):
        self.blink(self.table_canvas, self.game_title, 1000)

        self.window.bind('<Up>', self.upKey)
        self.window.bind('<Down>', self.downKey)
        self.window.bind('<Return>', self.enterKey)
        self.window.bind('<Button-1>', self.mouseClick)
        self.window.bind('<Motion>', self.mouseMotion)
