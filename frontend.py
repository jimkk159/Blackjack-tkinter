from time import sleep
from tkinter import *
from game import Blackjack
from PIL import Image, ImageTk
import pyglet

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

PIXEL_FONT = pyglet.font.add_file('./font/Pixels.ttf')

Upper_label_Font = ("Pixels", 120, "bold")
Lower_label_Font = ("Arial", 24, "bold")

PADDING = 20

window = Tk()
window.title("Jim's Blackjack Game")
window.minsize(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
window.config(padx=PADDING, pady=PADDING, bg="black")

game = Blackjack()

state = 0


def toggle_color(canvas, item, color_a, color_b):
    if canvas.itemcget(item, "fill") == color_a:
        canvas.itemconfig(item, fill=color_b)
    else:
        canvas.itemconfig(item, fill=color_a)


def change_icon_loc(canvas, item, state_, x, y):
    canvas.moveto(item, x, y + 50 * (state_ - 1))

def blink(canvas, item, delay_time):
    toggle_color(canvas, item, "black", "white")
    window.after(delay_time, blink, canvas, item, delay_time)


def switch_choice(pre_state, state_):
    canvas = table_canvas
    toggle_color(canvas, state_to_item(pre_state), "black", "white")
    toggle_color(canvas, state_to_item(state_), "black", "white")
    change_icon_loc(canvas, choice_icon, state_, 300+PADDING, 250-PADDING)


def state_to_item(state_):
    if state_ == 0:
        return start
    elif state_ == 1:
        return setting
    else:
        return quit_


def upKey(event):
    global state
    pre_state = state
    if state > 0:
        state -= 1
    switch_choice(pre_state, state)
    print("Up key pressed")


def downKey(event):
    global state
    pre_state = state
    if state < 2:
        state += 1
    switch_choice(pre_state, state)
    print("Down key pressed")


def leftKey(event):
    print("Left key pressed")


def rightKey(event):
    print("Right key pressed")


# def game_start_clicked():
#     hint_label.config(text="Game Start")
#     game.start()
#
# def game_quit_clicked():
#     hint_label.config(text="Game Quit")
#
# def hit_button_clicked():
#     hint_label.config(text="Hit")
#
#
# def stand_button_clicked():
#     hint_label.config(text="Stand")
#
#
# def double_button_clicked():
#     hint_label.config(text="Double Down")
#
#
# def fold_button_clicked():
#     hint_label.config(text="Fold")
#
#
# def split_button_clicked():
#     hint_label.config(text="Split")


# Label

# hint_label = Label(text="I am a Label", font=("Arial", 24, "bold"))
# hint_label.grid(column=1, row=0)
# hint_label.config(padx=20, pady=20)
#
# start_button = Button(text="Game Start", command=game_start_clicked)
# start_button.grid(column=2, row=1, padx=10, pady=10)
# start_button.config(padx=10, pady=10)
#
# quit_button = Button(text="Game End", command=game_quit_clicked)
# quit_button.grid(column=2, row=2, padx=10, pady=10)
# quit_button.config(padx=10, pady=10)
#
# hit_button = Button(text="Hit", command=hit_button_clicked)
# hit_button.grid(column=2, row=3, padx=10, pady=10)
# hit_button.config(padx=10, pady=10)
#
# stand_button = Button(text="Stand", command=stand_button_clicked)
# stand_button.grid(column=2, row=4, padx=10, pady=10)
# stand_button.config(padx=10, pady=10)
#
# double_button = Button(text="Double", command=double_button_clicked)
# double_button.grid(column=2, row=5, padx=10, pady=10)
# double_button.config(padx=10, pady=10)
#
# fold_button = Button(text="Fold", command=fold_button_clicked)
# fold_button.grid(column=2, row=6, padx=10, pady=10)
# fold_button.config(padx=10, pady=10)
#
# split_button = Button(text="Split", command=split_button_clicked)
# split_button.grid(column=2, row=7, padx=10, pady=10)
# split_button.config(padx=10, pady=10)


# Show Table

table_img = Image.open("./img/pixel-blackjack_big.png")
table_img = table_img.resize((800, 400))
table_pic = ImageTk.PhotoImage(table_img)
table_canvas = Canvas(window, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, highlightthickness=0)
table_canvas.create_image(400, 200, image=table_pic)

game_title = table_canvas.create_text(400, 100, text="Blackjack ", font=Upper_label_Font, fill="white")
title_icon = table_canvas.create_text(590, 115, text="♠", font=("Pixels", 80, "bold"))

start = table_canvas.create_text(350, 200, text="Start", font=Lower_label_Font, fill="white", anchor=W)
setting = table_canvas.create_text(350, 250, text="Setting", font=Lower_label_Font, anchor=W)
quit_ = table_canvas.create_text(350, 300, text="Quit", font=Lower_label_Font, anchor=W)

choice_icon = table_canvas.create_text(330, 200, text="♦", font=Lower_label_Font, fill="red")
table_canvas.grid(column=1, row=1)

blink(table_canvas, game_title, 1000)

window.bind('<Up>', upKey)
window.bind('<Down>', downKey)

window.mainloop()
