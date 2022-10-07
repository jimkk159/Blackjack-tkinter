from tkinter import *
from game import Blackjack

window = Tk()
window.title("Jim's Blackjack Game")
window.minsize(width=300, height=300)
window.config(padx=30, pady=30)

game = Blackjack()


def game_start_clicked():
    hint_label.config(text="Game Start")


def game_quit_clicked():
    hint_label.config(text="Game Quit")


def hit_button_clicked():
    hint_label.config(text="Hit")


def stand_button_clicked():
    hint_label.config(text="Stand")


def double_button_clicked():
    hint_label.config(text="Double Down")


def fold_button_clicked():
    hint_label.config(text="Fold")


def split_button_clicked():
    hint_label.config(text="Split")


# Label

hint_label = Label(text="I am a Label", font=("Arial", 24, "bold"))
hint_label.grid(column=1, row=0)
hint_label.config(padx=20, pady=20)

start_button = Button(text="Game Start", command=game_start_clicked)
start_button.grid(column=2, row=1, padx=10, pady=10)
start_button.config(padx=10, pady=10)

quit_button = Button(text="Game End", command=game_quit_clicked)
quit_button.grid(column=2, row=2, padx=10, pady=10)
quit_button.config(padx=10, pady=10)

hit_button = Button(text="Hit", command=hit_button_clicked)
hit_button.grid(column=2, row=3, padx=10, pady=10)
hit_button.config(padx=10, pady=10)

stand_button = Button(text="Stand", command=stand_button_clicked)
stand_button.grid(column=2, row=4, padx=10, pady=10)
stand_button.config(padx=10, pady=10)

double_button = Button(text="Double", command=double_button_clicked)
double_button.grid(column=2, row=5, padx=10, pady=10)
double_button.config(padx=10, pady=10)

fold_button = Button(text="Fold", command=fold_button_clicked)
fold_button.grid(column=2, row=6, padx=10, pady=10)
fold_button.config(padx=10, pady=10)

split_button = Button(text="Split", command=split_button_clicked)
split_button.grid(column=2, row=7, padx=10, pady=10)
split_button.config(padx=10, pady=10)

canvas = Canvas()

window.mainloop()
